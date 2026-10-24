
from collections import defaultdict
from typing import Dict, List


class ConversationMemory:

    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.conversations: Dict[str, List[dict]] = defaultdict(list)

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        if role not in {"user", "assistant"}:
            raise ValueError("Role must be 'user' or 'assistant'.")

        messages = self.conversations[session_id]

        messages.append({
            "role": role,
            "content": content,
        })

        if len(messages) > self.max_messages:
            self.conversations[session_id] = messages[-self.max_messages:]

    def get_history(self, session_id: str) -> List[dict]:
        return list(self.conversations.get(session_id, []))

    def clear(self, session_id: str) -> None:
        self.conversations.pop(session_id, None)
