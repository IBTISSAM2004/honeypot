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
- Fake admin login page
in chrome try
http://127.0.0.1
http://127.0.0.1/admin
- Path Traversal / LFI vulnerability**
Fake vulnerability test:
http://127.0.0.1/download?file=../../etc/passwd
  
  - SQL Injection vulnerability (intentional)
 /login?username=' OR '1'='1&password=' OR '1'='1
  
3/ FTP Honeypot
ftp 127.0.0.1
**View logs
All captured activity is stored in:
logs/attacks.log
**Stop the honeypot
Ctrl+C

