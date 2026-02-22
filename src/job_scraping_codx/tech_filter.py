TECH_INCLUDE_KEYWORDS = {
    "software engineer",
    "developer",
    "backend",
    "frontend",
    "full stack",
    "devops",
    "sre",
    "cloud",
    "python",
    "javascript",
    "typescript",
    "java",
    "go",
    "rust",
    "react",
    "node",
    "kubernetes",
    "aws",
    "hackathon",
    "internship",
    "machine learning",
    "data engineer",
    "mobile developer",
}

NON_TECH_EXCLUDE_KEYWORDS = {
    "sales",
    "accountant",
    "nurse",
    "driver",
    "chef",
    "civil engineer",
    "marketing executive",
    "real estate",
}


def relevance_score(text: str) -> float:
    normalized = text.lower()
    include_hits = sum(1 for k in TECH_INCLUDE_KEYWORDS if k in normalized)
    exclude_hits = sum(1 for k in NON_TECH_EXCLUDE_KEYWORDS if k in normalized)
    raw = (include_hits * 1.3) - (exclude_hits * 2)
    return max(0.0, min(1.0, raw / 8))


def relevance_label(score: float) -> str:
    if score >= 0.6:
        return "tech_relevant"
    if score >= 0.3:
        return "needs_review"
    return "not_tech_relevant"
