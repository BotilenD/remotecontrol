import socket
import pyautogui
import pickle
import struct
from PIL import ImageGrab
import io

SERVER_IP = "0.0.0.0"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, PORT))
server.listen(1)

print(f"Listening for connections on {SERVER_IP}:{PORT}...")


def handle_client(client_socket):
    try:
        while True:
            data_type = client_socket.recv(10).decode()

            if data_type == 'MOUSE':
                data = client_socket.recv(4096)
                events = pickle.loads(data)
                pyautogui.moveTo(events['x'], events['y'])
                if events['click']:
                    pyautogui.click()

            elif data_type == 'KEYBOARD':
                data = client_socket.recv(4096)
                events = pickle.loads(data)
                pyautogui.write(events['key'])

            elif data_type == 'SCREEN':
                screenshot = ImageGrab.grab()
                bytes_io = io.BytesIO()
                screenshot.save(bytes_io, format="JPEG")
                screenshot_data = bytes_io.getvalue()

                data = struct.pack("Q", len(screenshot_data)) + screenshot_data
                client_socket.sendall(data)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


while True:
    client_socket, addr = server.accept()
    print(f"Connection from {addr}")
    handle_client(client_socket)
