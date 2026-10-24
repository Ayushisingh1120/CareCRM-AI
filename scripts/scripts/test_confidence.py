from app.confidence.scorer import calculate_confidence


answer = (
    "A support agent cannot promise a refund "
    "before verifying refund eligibility."
)

sources = [
    {
        "source": "support_policy.md",
        "chunk_index": 1,
        "distance": 0.9745,
    },
    {
        "source": "support_policy.md",
        "chunk_index": 0,
        "distance": 1.3200,
    },
]

result = calculate_confidence(answer, sources)

print("\n=== CONFIDENCE TEST ===")
print("Answer:", answer)
print("Confidence:", result["score"])
print("Status:", result["status"])
print("Reasons:", result["reasons"])
print("Requires handoff:", result["requires_handoff"])