from flask import Flask, request, render_template
import time
import os
from flask import send_file
from web.sql_injection import sql_routes

app = Flask(
    __name__,
    template_folder="../web/templates",
    static_folder="../web/static"
)
sql_routes(app)

LOG_FILE = "logs/attacks.log"


def log_attack(action, detail):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()} | HTTP | {action} | {detail}\n")


@app.route("/")
def index():
    log_attack("VISIT", f"/ from {request.remote_addr}")
    return render_template("index.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        log_attack(
            "ADMIN_LOGIN",
            f"IP={request.remote_addr} USER={username} PASS={password}"
        )
        return "Access denied", 403

    log_attack("VISIT", f"/admin from {request.remote_addr}")
    return render_template("admin.html")

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

def start_http():
    print("[+] HTTP Honeypot listening on port 80")
    app.run(host="0.0.0.0", port=80, debug=False)

