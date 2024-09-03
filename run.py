# -*- coding: utf-8 -*-
import socket
import json

# Configuration
HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 25565       # Change this to the port you want
MOTD = "§aCustom MOTD§r\n§bNo real server here!"
MAX_PLAYERS = 0
CURRENT_PLAYERS = 0
KICK_MESSAGE = "§cSorry, this server is not available for connections."

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print(f"Listening on port {PORT}...")

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr}")

    try:
        data = conn.recv(1024)
        if data:
            # Check if it's a Server List Ping (0xFE for pre-1.7, modern versions have a different structure)
            if data[0] == 0xFE:
                # Send the MOTD response
                response = f"\xFF\x00{MOTD}\x00{CURRENT_PLAYERS}\x00{MAX_PLAYERS}"
                conn.sendall(response.encode('utf-16-be'))
            else:
                # If a client is trying to join, kick them with a custom message
                disconnect_packet = json.dumps({
                    "text": KICK_MESSAGE
                })
                response = b'\x00' + len(disconnect_packet).to_bytes(2, byteorder='big') + disconnect_packet.encode('utf-8')
                conn.sendall(response)
    except Exception as e:
        print(f"Error handling connection: {e}")
    finally:
        conn.close()
