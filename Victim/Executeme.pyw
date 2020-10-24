import time
import os

wificonn = False

while True:
    try:
        import httplibfix
    except:
        import http.client as httplib


    def checkInternetHttplib(url="www.google.com", timeout=3):
        conn = httplib.HTTPConnection(url, timeout=timeout)
        try:
            conn.request("HEAD", "/")
            conn.close()
            global wificonn
            if not wificonn:
                os.system("C:\\Documents\\test.txt")
                wificonn = True
            else:
                print("placeholder")
        except Exception:
            if wificonn:
                print("Wifi disconnected.")
                wificonn = False
                os.system("TASKKILL /F /IM notepad.exe")
            else:
                print("internet connection not yet detected")

        time.sleep(5)
