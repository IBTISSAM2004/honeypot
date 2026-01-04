from flask import Flask, request, render_template, redirect
import time
import os

# Flask App

app = Flask(
    __name__,
    template_folder="../web/templates",
    static_folder="../web/static"
)

# Logging

LOG_FILE = "logs/attacks.log"

def log_attack(action, detail):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()} | HTTP | {action} | {detail}\n")

# Routes

@app.route("/")
def index():
    log_attack("VISIT", f"/ from {request.remote_addr}")
    return render_template("index.html")


# Fake Admin Login 
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        log_attack(
            "ADMIN_LOGIN",
            f"IP={request.remote_addr} USER={username} PASS={password}"
        )

        return redirect("/admin/dashboard")

    return render_template("admin.html")


# Fake Admin Dashboard 
@app.route("/admin/dashboard")
def admin_dashboard():
    log_attack(
        "ADMIN_DASHBOARD",
        f"IP={request.remote_addr}"
    )
    return render_template("dashboard.html")


# LFI Honeypot 
@app.route("/download")
def download():
    filename = request.args.get("file", "")

    if "passwd" in filename:
        log_attack(
            "LFI_ATTEMPT",
            f"IP={request.remote_addr} FILE={filename}"
        )

        fake_passwd = """root:x:0:0:root:/root:/bin/bash
admin:x:1000:1000:admin:/home/admin:/bin/bash
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
mysql:x:999:999:mysql:/var/lib/mysql:/bin/false
"""
        return fake_passwd, 200, {"Content-Type": "text/plain"}

    return "File not found", 404


#  Brute Force Honeypot 
@app.route("/bruteforce", methods=["GET", "POST"])
def bruteforce():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        log_attack(
            "BRUTE_FORCE_ATTEMPT",
            f"IP={request.remote_addr} USER={username} PASS={password}"
        )

        return "Invalid username or password", 403

    return render_template("admin.html")
#SQL
import re

SQL_PATTERNS = [
    r"('|--|;|/\*|\*/|or\s+1=1|union\s+select|select\s+.*from)",
]

@app.route("/sql_login", methods=["GET", "POST"])
def sql_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        payload = f"{username} {password}"

        is_sql = any(
            re.search(p, payload, re.IGNORECASE)
            for p in SQL_PATTERNS
        )

        if is_sql:
            log_attack(
                "SQL_INJECTION",
                f"IP={request.remote_addr} PAYLOAD={payload}"
            )
            
            return "SQL syntax error near '' at line 1", 500

        
        return "Invalid credentials", 403

    return render_template("sql_login.html")

# Start Server

def start_http():
    print("[+] HTTP Honeypot listening on port 80")
    app.run(host="0.0.0.0", port=80, debug=False)
