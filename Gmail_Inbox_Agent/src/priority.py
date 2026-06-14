def assign_priority(email: dict) -> str:
    """Later, this will label emails as high, medium, or low priority."""
    text = f"{email.get('subject', '')} {email.get('snippet', '')}".lower()
    if "urgent" in text or "security" in text or "failed" in text:
        return "high"
    if "deadline" in text or "appointment" in text or "approval" in text:
        return "medium"
    return "low"
