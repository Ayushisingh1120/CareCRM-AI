
from datetime import datetime, timezone
from uuid import uuid4


class HumanHandoffService:
    def __init__(self):
        self.pending_handoffs = []

    def create_handoff(
        self,
        question: str,
        answer: str,
        confidence: float,
        reason: str,
        session_id: str = "default",
    ) -> dict:
        handoff = {
            "id": str(uuid4()),
            "session_id": session_id,
            "question": question,
            "answer": answer,
            "confidence": confidence,
            "reason": reason,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        self.pending_handoffs.append(handoff)
        return handoff

    def get_pending_handoffs(self) -> list[dict]:
        return [
            item
            for item in self.pending_handoffs
            if item["status"] == "pending"
        ]

    def resolve_handoff(self, handoff_id: str) -> dict | None:
        for item in self.pending_handoffs:
            if item["id"] == handoff_id:
                item["status"] = "resolved"
                return item

        return None
