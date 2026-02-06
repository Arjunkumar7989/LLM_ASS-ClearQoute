from db import get_connection
from ll import process_input
from validator import validate_sql


# -------------------------------------------------
# Execute SQL safely
# -------------------------------------------------
def execute_query(sql: str):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(sql)
        return cur.fetchall()

    except Exception as e:
        return None, str(e)

    finally:
        cur.close()
        conn.close()


# -------------------------------------------------
# Human-readable answer
# -------------------------------------------------
def format_answer(question, rows, assumptions):
    if not rows or rows[0][0] is None:
        return "No matching data found for this query."

    value = rows[0][0]

    answer = ""
    if "average" in question.lower():
        answer = f"The average repair cost is ₹{round(value, 2)}."
    else:
        answer = f"Query result: {rows}"

    if assumptions:
        answer += "\n\nAssumptions used:\n"
        for a in assumptions:
            answer += f"- {a}\n"

    return answer


# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    print("\n💬 Ask a question about vehicle repairs:")
    question = input("> ")

    sql, assumptions = process_input(question)

    if sql is None:
        print("\n❌ I could not confidently generate a SQL query for this question.")
        return

    print("\nGenerated SQL:")
    print(sql)

    # Validate SQL
    try:
        validate_sql(sql)
    except Exception as e:
        print("\n❌ Unsafe SQL blocked:")
        print(e)
        return

    # Execute SQL
    result = execute_query(sql)

    if isinstance(result, tuple):
        print("\n❌ SQL Execution Error:")
        print(result[1])
        return

    answer = format_answer(question, result, assumptions)

    print("\n✅ Answer:")
    print(answer)


if __name__ == "__main__":
    main()
