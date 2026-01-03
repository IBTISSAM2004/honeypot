from flask import request
from services.database import get_connection

def sql_routes(app):

    @app.route("/login", methods=["GET"])
    def login():
        username = request.args.get("username", "")
        password = request.args.get("password", "")

        conn = get_connection()
        cursor = conn.cursor()

        
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)

        result = cursor.fetchone()
        conn.close()

        
        if "'" in username or "--" in username or "OR" in username.upper():
            with open("logs/sql_injection.log", "a") as f:
                f.write(f"[SQLi] {request.remote_addr} -> {request.url}\n")

        if result:
            return "Login successful"
        else:
            return "Login failed"
