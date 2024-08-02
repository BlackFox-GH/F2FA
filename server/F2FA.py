from http.server import *
import os

print("[i] Starting F2FA...")
try:
    import pyotp
except ModuleNotFoundError:
    print("[!] Pyotp not found, installing...")
    import importlib
    import pip
    pip.main(['install', "pyotp"])
    globals()["pyotp"] = importlib.import_module("pyotp")
    print("[i] Pyotp intalled successfully!")

try:
    open("F2FA.conf","r").close()
except FileNotFoundError:
    print("[!] Config file not found, creating...")
    confFile=open("F2FA.conf","w")
    confFile.write("#Ez egy komment, mert #-el kezdődik\n#<id>:<private key> formátumban kell az adatokat hozzáadni\n#pl.:\n#TEAMS=xckshxfwcbzbmhlm\n#pyotp modul szükséges (pip install pyotp)\n")
    confFile.close()
    print("[i] Config file created successfully!")

PORT=51515

class F2FA(BaseHTTPRequestHandler):
    def do_GET(self):
        length = int(self.headers.get('content-length'))
        field_data = self.rfile.read(length).decode()
        key=None
        with open("F2FA.conf","r") as file:
            for line in file:
                if(not line.startswith("#")):
                    lineSplit=line.split("=")
                    if(lineSplit[0]==field_data):
                        key=pyotp.TOTP(("=".join(line.split("=")[1:])).strip()).now()
                        break
        if(key==None):
            self.send_response(418)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write("NOTFOUND".encode())
        else:
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(key.encode())

os.chdir(os.path.dirname(__file__))
port = HTTPServer(('127.0.0.1', PORT), F2FA)
port.allow_reuse_address=True
print("[i] Server started at port "+str(PORT))
print("[i] F2FA started successfully.")
try:
    port.serve_forever()
except KeyboardInterrupt:
    port.server_close()
    print("[i] Server shutdown successfully")
print("[i] F2FA has shut down successfully.")

