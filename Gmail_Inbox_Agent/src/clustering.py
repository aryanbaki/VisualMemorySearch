def group_similar_emails(emails: list[dict]) -> list[dict]:
    """Later, this will group similar emails using text features and clustering."""
    return [
        {
            "group_id": index + 1,
            "emails": [email],
            "summary": "Ungrouped demo placeholder",
        }
        for index, email in enumerate(emails)
    ]
