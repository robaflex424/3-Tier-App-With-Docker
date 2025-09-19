from flask import Flask, request, jsonify
import mysql.connector
import redis
import os

app = Flask(__name__)

# Database connection settings (use env vars in Docker later)
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_NAME = os.getenv("DB_NAME", "mysql_db")
DB_USER = os.getenv("DB_USER", "mysqluser")
DB_PASS = os.getenv("DB_PASS", "mysqlpassword")

# Redis connection (optional)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

@app.route("/add", methods=["POST"])
def add_user():
    data = request.json
    name = data.get("name", "Alice")  # Use payload or default

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    cur.close()
    conn.close()

    # Invalidate cache
    redis_client.delete("users_cache")

    return jsonify({"message": f"User {name} added!"})


@app.route("/users", methods=["GET"])
def get_users():
    # Try Redis cache first
    cached_users = redis_client.get("users_cache")
    if cached_users:
        return jsonify({"users": eval(cached_users), "source": "cache"})

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = [{"id": r[0], "name": r[1]} for r in rows]

    # Save to cache
    redis_client.set("users_cache", str(users), ex=30)  # cache 30 sec

    return jsonify({"users": users, "source": "db"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
