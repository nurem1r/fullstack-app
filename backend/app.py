from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

# создаём таблицу при старте
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route("/api/data", methods=["GET"])
def get_data():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM students;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{"id": r[0], "name": r[1]} for r in rows])

@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.json
    name = data.get("name")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name) VALUES (%s) RETURNING id;", (name,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_id, "name": name})

@app.route("/api/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "deleted"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
