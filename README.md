## How to Run

###  Clone the repository
```bash
git clone git@github.com:IBTISSAM2004/honeypot.git
cd honeypot
Install requirements
pip install flask paramiko
Run the honeypot
The honeypot requires root privileges to listen on ports 80 and 21.
sudo python3 main.py
if everything works correctly, you should see:
[+] HTTP Honeypot listening on port 80
[+] SSH Honeypot listening on port 2222

Test the services
1/ SSH
ssh root@127.0.0.1 -p 2222
Enter any password
Try commands
ls
pwd
id
sudo -l
2/ HTTP Honeypot
admin — Fake Admin Login
Simulates an administrative login page.
Accepts any username and password.
Redirects the attacker to a fake admin dashboard.
Used to collect credentials and observe attacker behavior.
 — Fake Admin Dashboard
Simulates an internal admin control panel.
Displays fake system information.
No real administrative functionality is implemented.
Designed to keep the attacker engaged.
in chrome try
http://127.0.0.1
http://127.0.0.1/admin
http://127.0.0.1/admin/dashboard

bruteforce — Brute Force Simulation
Simulates a login endpoint vulnerable to brute force attacks.
Always returns invalid credentials.
Each login attempt is recorded.
http://127.0.0.1/bruteforce

- Path Traversal / LFI vulnerability**
download — Local File Inclusion (LFI)
Simulates an LFI vulnerability.
When attempting to access /etc/passwd, a fake file is returned.
Used to detect directory traversal and file inclusion attempts.
Fake vulnerability test:
http://127.0.0.1/download?file=../../etc/passwd
  
  - SQL Injection vulnerability 
 sql_login — SQL Injection Honeypot
Dedicated endpoint for SQL injection testing.
Detects common SQL injection patterns.
Returns realistic SQL error messages.
No real database interaction is performed.
http://127.0.0.1/sql_login

**All detected HTTP attacks are logged in:logs/attacks.log **
  
3/ FTP Honeypot
ftp 127.0.0.1
**View logs
All captured activity is stored in:
logs/attacks.log
**Stop the honeypot
Ctrl+C

