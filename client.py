import socket
import pyautogui
import pickle
import struct
import io
from PIL import Image
import time

SERVER_IP = "192.168.1.5"
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))


def send_mouse_data():
    while True:
        try:
            x, y = pyautogui.position()
            click = pyautogui.mouseDown()
            events = {'type': 'mouse', 'x': x, 'y': y, 'click': click}
            data = pickle.dumps(events)
            client.sendall("MOUSE".ljust(10).encode() + data)
            time.sleep(0.1)

        except Exception as e:
            print(f"Error in mouse sending: {e}")
            break


def send_keyboard_data():
    try:
        while True:
            key = input("Type something: ")
            events = {'type': 'keyboard', 'key': key}
            data = pickle.dumps(events)
            client.sendall("KEYBOARD".ljust(10).encode() + data)

    except KeyboardInterrupt:
        client.close()


def receive_screenshots():
    try:
        while True:
            client.sendall("SCREEN".ljust(10).encode())
            packed_msg_size = client.recv(8)
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            data = b""
            while len(data) < msg_size:
                data += client.recv(4096)

            bytes_io = io.BytesIO(data)
            screenshot = Image.open(bytes_io)
            screenshot.show()

            time.sleep(0.5)

    except Exception as e:
        print(f"Error in receiving screenshots: {e}")
        client.close()


if __name__ == "__main__":
    choice = input("Start capturing (m)ouse, (k)eyboard, or (s)creen? ")

    if choice == 'm':
        send_mouse_data()
    elif choice == 'k':
        send_keyboard_data()
    elif choice == 's':
        receive_screenshots()
