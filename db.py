import sqlite3
import csv

DB_NAME = "vehicle_damage.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    with open("sql/schema.sql", "r") as f:
        cur.executescript(f.read())
    conn.commit()
    conn.close()


# -------- vehicle_cards --------
def import_vehicle_cards():
    conn = get_connection()
    cur = conn.cursor()

    with open("Data/vehicle_cards.csv", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                """
                INSERT OR REPLACE INTO vehicle_cards
                (card_id, vehicle_type, manufacturer, model, manufacture_year, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    row["card_id"],
                    row["vehicle_type"],
                    row["manufacturer"],
                    row["model"],
                    int(row["manufacture_year"]),
                    row["created_at"]
                )
            )

    conn.commit()
    conn.close()


# -------- damage_detections --------
def import_damage_detections():
    conn = get_connection()
    cur = conn.cursor()

    severity_map = {
        "minor": 1,
        "moderate": 3,
        "severe": 5
    }

    with open("Data/damage_detections.csv", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            severity_value = severity_map.get(row["severity"].lower(), 0)

            cur.execute(
                """
                INSERT OR REPLACE INTO damage_detections
                (damage_id, card_id, panel_name, damage_type, severity, confidence, detected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["damage_id"],
                    row["card_id"],
                    row["panel_name"].lower(),
                    row["damage_type"].lower(),
                    severity_value,
                    float(row["confidence"]),
                    row["detected_at"]
                )
            )

    conn.commit()
    conn.close()


# -------- repairs --------
def import_repairs():
    conn = get_connection()
    cur = conn.cursor()

    with open("Data/repairs.csv", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            approved_value = 1 if row["approved"].upper() == "TRUE" else 0
            repair_cost_value = (
                float(row["repair_cost"])
                if row["repair_cost"].strip() != ""
                else 0.0
            )

            cur.execute(
                """
                INSERT OR REPLACE INTO repairs
                (repair_id, card_id, panel_name, repair_action, repair_cost, approved, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["repair_id"],
                    row["card_id"],
                    row["panel_name"].lower(),
                    row["repair_action"].lower(),
                    repair_cost_value,
                    approved_value,
                    row["created_at"]
                )
            )

    conn.commit()
    conn.close()


# -------- quotes --------
def import_quotes():
    conn = get_connection()
    cur = conn.cursor()

    with open("Data/quotes.csv", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_cost_value = (
                float(row["total_estimated_cost"])
                if row["total_estimated_cost"].strip() != ""
                else 0.0
            )

            cur.execute(
                """
                INSERT OR REPLACE INTO quotes
                (quote_id, card_id, total_estimated_cost, currency, generated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    row["quote_id"],
                    row["card_id"],
                    total_cost_value,
                    row["currency"],
                    row["generated_at"]
                )
            )

    conn.commit()
    conn.close()
