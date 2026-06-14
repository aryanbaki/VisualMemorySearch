def parse_email_message(raw_message: dict) -> dict:
    """Later, this will normalize raw Gmail message payloads into app-friendly rows."""
    return {
        "id": raw_message.get("id", ""),
        "from_email": raw_message.get("from_email", ""),
        "subject": raw_message.get("subject", ""),
        "date": raw_message.get("date", ""),
        "snippet": raw_message.get("snippet", ""),
        "body": raw_message.get("body", ""),
    }


def extract_search_text(email_row: dict) -> str:
    """Combine fields that will eventually be used for clustering and priority scoring."""
    return " ".join(
        str(email_row.get(field, ""))
        for field in ("from_email", "subject", "snippet", "body")
    ).strip()
