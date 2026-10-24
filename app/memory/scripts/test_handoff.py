
from app.confidence.handoff import HumanHandoffService

service = HumanHandoffService()

handoff = service.create_handoff(
    question="My account may have been compromised.",
    answer="This requires review by a human support agent.",
    confidence=0.30,
    reason="Possible account security issue",
    session_id="session_001",
)

print("=== CREATED HANDOFF ===")
print(handoff)

print("\n=== PENDING HANDOFFS ===")
print(service.get_pending_handoffs())

resolved = service.resolve_handoff(handoff["id"])

print("\n=== RESOLVED HANDOFF ===")
print(resolved)
