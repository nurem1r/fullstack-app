from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Backend работает!"

@app.route("/api/data", methods=["GET"])
def get_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks ORDER BY id")
    rows = cur.fetchall()

    tasks = [{"id": row[0], "title": row[1]} for row in rows]

    cur.close()
    conn.close()

    return jsonify(tasks)

@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.json
    title = data.get("title")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (title) VALUES (%s) RETURNING id",
        (title,)
    )

    new_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id": new_id,
        "title": title
    })

@app.route("/api/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
