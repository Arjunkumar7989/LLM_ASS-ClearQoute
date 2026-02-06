# -------------------------------
# Panel synonym mapping
# -------------------------------
PANEL_SYNONYMS = {
    "rear bumper": ["rear bumper", "back bumper", "rear side"],
    "front bumper": ["front bumper"],
    "front panel": ["front panel", "front side panel"]
}


def normalize_panel(text: str):
    """
    Maps user-friendly panel terms to canonical DB values.
    If multiple matches exist, returns the most specific one.
    """
    text = text.lower()
    matches = []

    for panel, aliases in PANEL_SYNONYMS.items():
        for alias in aliases:
            if alias in text:
                matches.append(panel)

    if not matches:
        return None

    # Prefer longer / more specific panel names
    return sorted(matches, key=len, reverse=True)[0]


# -------------------------------
# Time filter (table-aware)
# -------------------------------
def extract_time_filter(text: str, table: str):
    """
    Extracts date filters from natural language.
    Uses rolling windows unless calendar month explicitly mentioned.
    """
    text = text.lower()

    column = "created_at" if table == "repairs" else "detected_at"

    if "last 7 days" in text:
        return f"date({column}) >= date('now', '-7 day')"

    if "last 30 days" in text or "recent" in text:
        return f"date({column}) >= date('now', '-30 day')"

    if "this month" in text:
        return f"strftime('%Y-%m', {column}) = strftime('%Y-%m', 'now')"

    return None


# -------------------------------
# Main NL → SQL function
# -------------------------------
def process_input(question: str):
    """
    Converts natural language question into safe, read-only SQL.
    Returns:
        sql_query (str)
        assumptions (list[str])
    """
    q = question.lower()
    assumptions = []

    # -------------------------------------------------
    # Average repair cost
    # -------------------------------------------------
    if "average" in q and "repair cost" in q:
        sql = """
        SELECT AVG(repair_cost)
        FROM repairs
        """

        conditions = []

        # Panel handling
        panel = normalize_panel(q)
        if panel:
            conditions.append(f"panel_name = '{panel}'")

        # Severity assumption (not specified)
        assumptions.append("All damage severities were considered")

        # Time handling
        time_filter = extract_time_filter(q, "repairs")
        if time_filter:
            conditions.append(time_filter)
        else:
            conditions.append("date(created_at) >= date('now', '-30 day')")
            assumptions.append(
                "Time range not specified, defaulted to last 30 days"
            )

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        return sql.strip(), assumptions

    # -------------------------------------------------
    # Count severe damages
    # -------------------------------------------------
    if "severe" in q and "damage" in q:
        sql = """
        SELECT COUNT(*)
        FROM damage_detections
        WHERE severity = 5
        """

        # Panel handling
        panel = normalize_panel(q)
        if panel:
            sql += f" AND panel_name = '{panel}'"

        # Time handling
        time_filter = extract_time_filter(q, "damage_detections")
        if time_filter:
            sql += f" AND {time_filter}"
        else:
            sql += " AND date(detected_at) >= date('now', '-30 day')"
            assumptions.append(
                "Time range not specified, defaulted to last 30 days"
            )

        return sql.strip(), assumptions

    # -------------------------------------------------
    # Unsupported query
    # -------------------------------------------------
    return None, []
