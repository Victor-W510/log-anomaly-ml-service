from db import get_connection

def test_connection():
    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute("SELECT * from logs")
            result = cursor.fetchone()

        conn.close()

        print("✅ DB CONNECTION OK")
        print("Result:", result)

    except Exception as e:
        print("❌ DB CONNECTION FAILED")
        print("Error:", e)


if __name__ == "__main__":
    test_connection()