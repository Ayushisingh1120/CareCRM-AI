
import json
import logging
from typing import Any

from ollama import chat

from app.agents.tools import (
    get_customer,
    get_ticket,
    get_customer_tickets,
    create_ticket,
    search_knowledge_base,
)
from app.agents.safety import requires_confirmation
from app.confidence.scorer import calculate_confidence
from app.confidence.handoff import HumanHandoffService
from app.memory.conversation_memory import ConversationMemory

logger = logging.getLogger(__name__)


class CareCRMAgent:
    def __init__(
        self,
        model: str = "qwen3:8b",
        max_tool_iterations: int = 8,
    ):
        self.model = model
        self.max_tool_iterations = max_tool_iterations

        self.memory = ConversationMemory(max_messages=20)
        self.handoff_service = HumanHandoffService()

        # Pending write actions are stored per conversation session.
        self.pending_actions: dict[str, dict[str, Any]] = {}

        self.available_tools = {
            "get_customer": get_customer,
            "get_ticket": get_ticket,
            "get_customer_tickets": get_customer_tickets,
            "create_ticket": create_ticket,
            "search_knowledge_base": search_knowledge_base,
        }

        self.tool_definitions = [
            {
                "type": "function",
                "function": {
                    "name": "get_customer",
                    "description": "Retrieve a customer by customer ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_id": {
                                "type": "integer",
                                "description": "The customer ID.",
                            }
                        },
                        "required": ["customer_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_ticket",
                    "description": "Retrieve a ticket by ticket ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ticket_id": {
                                "type": "string",
                                "description": "Ticket ID, such as TKT-001.",
                            }
                        },
                        "required": ["ticket_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_customer_tickets",
                    "description": "Retrieve all tickets belonging to a customer.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_id": {
                                "type": "integer",
                                "description": "The customer ID.",
                            }
                        },
                        "required": ["customer_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "create_ticket",
                    "description": (
                        "Create a support ticket. This is a write action "
                        "and requires user confirmation."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_id": {
                                "type": "integer",
                                "description": "The customer ID.",
                            },
                            "subject": {
                                "type": "string",
                                "description": "The ticket subject.",
                            },
                            "description": {
                                "type": "string",
                                "description": "Details of the issue.",
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["Low", "Medium", "High", "Critical"],
                                "description": "Ticket priority.",
                            },
                        },
                        "required": [
                            "customer_id",
                            "subject",
                            "description",
                            "priority",
                        ],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_knowledge_base",
                    "description": (
                        "Search support policies and documentation. "
                        "Use this for policy, refund, and support-process questions."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The question to search for.",
                            }
                        },
                        "required": ["question"],
                    },
                },
            },
        ]

    @staticmethod
    def _as_dict(value: Any) -> dict:
        """Convert an Ollama object or dictionary into a dictionary."""
        if isinstance(value, dict):
            return value

        if hasattr(value, "model_dump"):
            return value.model_dump()

        if hasattr(value, "dict"):
            return value.dict()

        return {}

    @staticmethod
    def _tool_call_details(tool_call: Any) -> tuple[str, dict]:
        """Read a tool call from an Ollama response."""
        call_data = CareCRMAgent._as_dict(tool_call)
        function_data = call_data.get("function", {})

        if not function_data and hasattr(tool_call, "function"):
            function_obj = tool_call.function
            function_data = {
                "name": getattr(function_obj, "name", ""),
                "arguments": getattr(function_obj, "arguments", {}),
            }

        name = function_data.get("name", "")
        arguments = function_data.get("arguments", {})

        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError:
                arguments = {}

        if not isinstance(arguments, dict):
            arguments = {}

        return name, arguments

    @staticmethod
    def _serialize(value: Any) -> str:
        """Serialize tool output safely for the LLM."""
        try:
            return json.dumps(value, default=str, ensure_ascii=False)
        except (TypeError, ValueError):
            return json.dumps({"result": str(value)})

    @staticmethod
    def _decode_tool_result(result: Any) -> Any:
        """Decode JSON returned by a tool when possible."""
        if isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return result

        return result

    @staticmethod
    def _extract_sources(tool_results: list[dict]) -> list[dict]:
        """Extract retrieved knowledge-base sources from tool results."""
        sources = []

        for result in tool_results:
            if result.get("tool_name") != "search_knowledge_base":
                continue

            payload = CareCRMAgent._decode_tool_result(
                result.get("result")
            )

            if not isinstance(payload, dict):
                continue

            retrieved_sources = payload.get("sources", [])

            if isinstance(retrieved_sources, list):
                sources.extend(
                    source
                    for source in retrieved_sources
                    if isinstance(source, dict)
                )

        return sources

    @staticmethod
    def _is_sensitive_request(question: str) -> str | None:
        """
        Detect explicit account-security concerns in the user's question.

        This is a basic keyword rule, not a comprehensive security classifier.
        """
        question_lower = question.lower()

        security_keywords = [
            "account security",
            "suspicious activity",
            "account compromised",
            "unauthorized access",
            "unauthorised access",
            "account hacked",
            "someone hacked my account",
            "someone accessed my account",
        ]

        for keyword in security_keywords:
            if keyword in question_lower:
                return keyword

        return None

    @staticmethod
    def _is_confirmation(text: str) -> bool:
        return text.strip().lower() in {
            "yes",
            "yes please",
            "confirm",
            "confirmed",
            "proceed",
            "go ahead",
            "do it",
            "approve",
        }

    @staticmethod
    def _is_cancellation(text: str) -> bool:
        return text.strip().lower() in {
            "no",
            "no thanks",
            "cancel",
            "cancel it",
            "don't",
            "do not",
            "stop",
            "abort",
        }

    def _execute_tool(
        self,
        tool_name: str,
        arguments: dict,
    ) -> Any:
        """Execute a registered tool and return its result."""
        tool_function = self.available_tools.get(tool_name)

        if tool_function is None:
            return {"error": f"Unknown tool: {tool_name}"}

        try:
            return tool_function(**arguments)
        except Exception as exc:
            logger.exception("Tool execution failed: %s", tool_name)
            return {
                "error": f"Tool '{tool_name}' failed.",
                "details": str(exc),
            }

    def _create_handoff(
        self,
        question: str,
        answer: str,
        confidence: float,
        reason: str,
        session_id: str,
    ) -> str:
        """Create a handoff record and return a user-facing message."""
        handoff = self.handoff_service.create_handoff(
            question=question,
            answer=answer,
            confidence=confidence,
            reason=reason,
            session_id=session_id,
        )

        return (
            "This request needs review by a human support agent.\n\n"
            f"Reason: {handoff['reason']}\n"
            f"Handoff ID: {handoff['id']}\n"
            f"Status: {handoff['status']}"
        )

    def _handle_pending_action(
        self,
        question: str,
        session_id: str,
    ) -> str | None:
        """Handle confirmation or cancellation of a pending write action."""
        pending = self.pending_actions.get(session_id)

        if not pending:
            return None

        if self._is_cancellation(question):
            self.pending_actions.pop(session_id, None)
            return "The action has been cancelled. No changes were made."

        if not self._is_confirmation(question):
            return (
                "There is a pending action awaiting confirmation. "
                "Reply 'yes' to proceed or 'cancel' to discard it."
            )

        tool_name = pending["tool_name"]
        arguments = pending["arguments"]

        # Remove the pending action before execution to prevent duplicates.
        self.pending_actions.pop(session_id, None)

        result = self._execute_tool(tool_name, arguments)

        result_data = self._decode_tool_result(result)

        if isinstance(result_data, dict) and result_data.get("error"):
            return (
                "I couldn't complete the requested action. "
                f"Details: {result_data.get('error')}"
            )

        return (
            "The action has been completed.\n\n"
            f"Result: {self._serialize(result_data)}"
        )

    def run(
        self,
        question: str,
        session_id: str = "default",
    ) -> str:
        """Process a user question using memory, tools, and safety checks."""
        if not question or not question.strip():
            return "Please enter a question."

        question = question.strip()

        try:
            # Handle a previously requested write action first.
            if session_id in self.pending_actions:
                result = self._handle_pending_action(
                    question,
                    session_id,
                )

                if result is not None:
                    self.memory.add_message(
                        session_id, "user", question
                    )
                    self.memory.add_message(
                        session_id, "assistant", result
                    )
                    return result

            # Security-sensitive questions go directly to human review.
            sensitive_keyword = self._is_sensitive_request(question)

            if sensitive_keyword:
                response = self._create_handoff(
                    question=question,
                    answer="Escalated for human review.",
                    confidence=0.0,
                    reason=(
                        "Sensitive issue detected: "
                        f"{sensitive_keyword}"
                    ),
                    session_id=session_id,
                )

                self.memory.add_message(
                    session_id, "user", question
                )
                self.memory.add_message(
                    session_id, "assistant", response
                )
                return response

            history = self.memory.get_history(session_id)

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are CareCRM AI, a customer support copilot. "
                        "Use get_customer, get_ticket, and "
                        "get_customer_tickets for CRM lookups. "
                        "Use search_knowledge_base for policy and "
                        "support-documentation questions, including "
                        "refund eligibility. Never invent policy details "
                        "or promise a refund unless the retrieved policy "
                        "explicitly supports it. Use create_ticket when "
                        "the user requests ticket creation, but wait for "
                        "confirmation before executing write actions. "
                        "If retrieved information is insufficient, "
                        "do not fabricate an answer."
                    ),
                }
            ]

            messages.extend(history)
            messages.append({
                "role": "user",
                "content": question,
            })

            tool_results = []

            for _ in range(self.max_tool_iterations):
                response = chat(
                    model=self.model,
                    messages=messages,
                    tools=self.tool_definitions,
                )

                assistant_message = response.message
                messages.append(assistant_message)

                tool_calls = (
                    getattr(assistant_message, "tool_calls", None) or []
                )

                if not tool_calls:
                    answer = (
                        getattr(assistant_message, "content", None)
                        or "I could not generate a response."
                    )

                    sources = self._extract_sources(tool_results)

                    self.memory.add_message(
                        session_id, "user", question
                    )

                    # Confidence scoring is only applied to answers
                    # that actually used the knowledge-base tool.
                    if any(
                        item["tool_name"] == "search_knowledge_base"
                        for item in tool_results
                    ):
                        confidence = calculate_confidence(
                            answer,
                            sources,
                        )

                        if confidence.get("requires_handoff", False):
                            handoff_response = self._create_handoff(
                                question=question,
                                answer=answer,
                                confidence=confidence["score"],
                                reason="; ".join(
                                    confidence.get("reasons", [])
                                ),
                                session_id=session_id,
                            )

                            self.memory.add_message(
                                session_id,
                                "assistant",
                                handoff_response,
                            )
                            return handoff_response

                    self.memory.add_message(
                        session_id,
                        "assistant",
                        answer,
                    )
                    return answer

                for tool_call in tool_calls:
                    tool_name, arguments = self._tool_call_details(
                        tool_call
                    )

                    if tool_name not in self.available_tools:
                        tool_result = {
                            "error": f"Unknown tool: {tool_name}"
                        }
                    elif requires_confirmation(tool_name):
                        self.pending_actions[session_id] = {
                            "tool_name": tool_name,
                            "arguments": arguments,
                        }

                        confirmation_message = (
                            "Please confirm before I create this ticket.\n\n"
                            f"Details: {self._serialize(arguments)}\n\n"
                            "Reply 'yes' to proceed or 'cancel' to discard."
                        )

                        self.memory.add_message(
                            session_id, "user", question
                        )
                        self.memory.add_message(
                            session_id,
                            "assistant",
                            confirmation_message,
                        )

                        return confirmation_message
                    else:
                        tool_result = self._execute_tool(
                            tool_name,
                            arguments,
                        )

                    tool_results.append({
                        "tool_name": tool_name,
                        "result": tool_result,
                    })

                    messages.append({
                        "role": "tool",
                        "content": self._serialize(tool_result),
                    })

            return (
                "I could not complete the request within the allowed "
                "number of tool calls. Please try again."
            )

        except Exception:
            logger.exception("CareCRM agent failed")
            return (
                "Sorry, I encountered an internal error while "
                "processing your request. Please try again."
            )
