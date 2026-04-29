from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    url = DATABASE_URL
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(url)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

@app.route("/api/data", methods=["GET"])
def get_data():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM students")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(rows)

@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.json
    name = data.get("name")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("INSERT INTO students (name) VALUES (%s)", (name,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"status": "ok"})

@app.route("/api/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id = %s", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

