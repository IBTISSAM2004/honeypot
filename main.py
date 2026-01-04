from services.ssh_service import start_ssh
from services.http_service import start_http
from services.ftp_service import start_ftp
import threading


ftp_thread = threading.Thread(target=start_ftp, daemon=True)
ftp_thread.start()

threading.Thread(target=start_ssh).start()
threading.Thread(target=start_http).start()

