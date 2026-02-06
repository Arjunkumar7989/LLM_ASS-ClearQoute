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
