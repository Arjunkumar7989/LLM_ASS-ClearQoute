# -------------------------------
# Panel synonym mapping
# -------------------------------
PANEL_SYNONYMS = {
    "rear bumper": ["rear bumper", "back bumper", "rear side"],
    "front bumper": ["front bumper", "front side"],
    "front panel": ["front panel", "front side panel"]
}


def normalize_panel(text: str):
    text = text.lower()
    for panel, aliases in PANEL_SYNONYMS.items():
        for alias in aliases:
            if alias in text:
                return panel
    return None


# -------------------------------
# Time filter (table-aware)
# -------------------------------
def extract_time_filter(text: str, table: str):
    text = text.lower()

    # choose correct date column
    column = "created_at" if table == "repairs" else "detected_at"

    if "last 30 days" in text:
        return f"date({column}) >= date('now', '-30 day')"

    if "last 7 days" in text:
        return f"date({column}) >= date('now', '-7 day')"

    if "this month" in text:
        return f"strftime('%Y-%m', {column}) = strftime('%Y-%m', 'now')"

    return None


# -------------------------------
# Main NL → SQL function
# -------------------------------
def process_input(question: str):
    q = question.lower()

    # ---- Average repair cost ----
    if "average" in q and "repair cost" in q:
        sql = """
        SELECT AVG(repair_cost)
        FROM repairs
        """

        conditions = []

        panel = normalize_panel(q)
        if panel:
            conditions.append(f"panel_name = '{panel}'")

        time_filter = extract_time_filter(q, "repairs")
        if time_filter:
            conditions.append(time_filter)

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        return sql.strip()

    # ---- Count severe damages ----
    if "severe" in q and "damage" in q:
        sql = """
        SELECT COUNT(*)
        FROM damage_detections
        WHERE severity >= 4
        """

        panel = normalize_panel(q)
        if panel:
            sql += f" AND panel_name = '{panel}'"

        time_filter = extract_time_filter(q, "damage_detections")
        if time_filter:
            sql += f" AND {time_filter}"

        return sql.strip()

    return None
