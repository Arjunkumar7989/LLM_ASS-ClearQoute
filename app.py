from db import (
    create_tables,
    import_vehicle_cards,
    import_damage_detections,
    import_repairs,
    import_quotes,
    get_connection
)
from ll import process_input


def main():
    # DB setup
    create_tables()
    import_vehicle_cards()
    import_damage_detections()
    import_repairs()
    import_quotes()
    print("✅ All CSV datasets imported successfully into database")

    # 🔥 CHANGE QUESTION HERE FOR DEMO
    question = "What is the average repair cost?"
    # question = "What is the average rear bumper repair cost in last 30 days?"

    print("\nUser Question:")
    print(question)

    sql = process_input(question)
    print("\nGenerated SQL:")
    print(sql)

    if sql is None:
        print("❌ Could not generate SQL")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(sql)
        result = cur.fetchall()

        if result[0][0] is None:
            print("\nQuery Result:")
            print("No matching data found for this query.")
        else:
            print("\nQuery Result:")
            print(result)

    except Exception as e:
        print("❌ SQL Execution Error:", e)

    conn.close()


if __name__ == "__main__":
    main()
from db import (
    create_tables,
    import_vehicle_cards,
    import_damage_detections,
    import_repairs,
    import_quotes,
    get_connection
)
from ll import process_input


def setup_database():
    """
    Run once to setup DB and import CSVs.
    In real systems, this would be a separate script.
    """
    create_tables()
    import_vehicle_cards()
    import_damage_detections()
    import_repairs()
    import_quotes()
    print("✅ Database setup completed (tables + CSV imports)")


def execute_query(sql):
    """
    Executes ONLY safe SELECT queries and returns results.
    """
    if not sql.strip().lower().startswith("select"):
        return None, "Only SELECT queries are allowed for safety reasons."

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(sql)
        rows = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]
        return rows, col_names

    except Exception as e:
        return None, str(e)

    finally:
        cur.close()
        conn.close()


def format_answer(question, rows, col_names):
    """
    Converts raw SQL output into user-friendly text.
    """
    if not rows or rows[0][0] is None:
        return "No matching data found for this query."

    value = rows[0][0]

    if "average" in question.lower():
        return f"The average repair cost is {round(value, 2)}."

    return f"Query result: {rows}"


def main():
    # ⚠️ Run setup only once (comment after first run)
    # setup_database()

    print("\n💬 Ask a question about vehicle repairs:")
    question = input("> ")

    print("\nUser Question:")
    print(question)

    sql = process_input(question)

    if sql is None:
        print("\n❌ I could not confidently generate a SQL query for this question.")
        return

    print("\nGenerated SQL:")
    print(sql)

    rows, meta = execute_query(sql)

    if rows is None:
        print("\n❌ Unable to execute query safely:")
        print(meta)
        return

    answer = format_answer(question, rows, meta)

    print("\n✅ Answer:")
    print(answer)


if __name__ == "__main__":
    main()
