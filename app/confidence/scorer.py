
from app.confidence.rules import (
    CONFIDENCE_THRESHOLD,
    ESCALATION_KEYWORDS,
)


def calculate_confidence(answer: str, sources: list[dict]) -> dict:
    """
    Estimate answer confidence using retrieval quality and grounding signals.

    This is a heuristic score, not a calibrated probability.
    """

    if not answer or not answer.strip():
        return {
            "score": 0.0,
            "status": "low",
            "reasons": ["The answer is empty."],
            "requires_handoff": True,
        }

    answer_lower = answer.lower()

    # Escalate only when a sensitive keyword is actually present
    # in the answer being evaluated.
    for keyword in ESCALATION_KEYWORDS:
        if keyword.lower() in answer_lower:
            return {
                "score": 0.0,
                "status": "low",
                "reasons": [
                    f"Sensitive issue detected: {keyword}"
                ],
                "requires_handoff": True,
            }

    # Require retrieved knowledge for policy answers.
    if not sources:
        return {
            "score": 0.0,
            "status": "low",
            "reasons": [
                "No knowledge-base sources were retrieved."
            ],
            "requires_handoff": True,
        }

    distances = [
        source.get("distance")
        for source in sources
        if isinstance(source, dict)
        and isinstance(source.get("distance"), (int, float))
    ]

    if not distances:
        return {
            "score": 0.0,
            "status": "low",
            "reasons": [
                "Retrieval quality could not be evaluated."
            ],
            "requires_handoff": True,
        }

    best_distance = min(distances)

    if best_distance <= 1.0:
        retrieval_score = 0.90
    elif best_distance <= 1.2:
        retrieval_score = 0.75
    elif best_distance <= 1.5:
        retrieval_score = 0.55
    else:
        retrieval_score = 0.30

    score = min(
        1.0,
        retrieval_score + (0.05 if len(sources) >= 2 else 0.0),
    )
    score = round(score, 2)

    reasons = [
        f"Best retrieval distance: {best_distance:.3f}",
        f"Retrieved sources: {len(sources)}",
    ]

    requires_handoff = score < CONFIDENCE_THRESHOLD

    return {
        "score": score,
        "status": "high" if not requires_handoff else "low",
        "reasons": reasons,
        "requires_handoff": requires_handoff,
    }
