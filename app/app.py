from flask import Flask
import redis
import os

app = Flask(__name__)

# Connect to Redis container
r = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379, db=0)

@app.route("/")
def counter():
    count = r.incr("hits")
    return f"<h1>Visitor count: {count}</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)