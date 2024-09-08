import socket
import threading
import websockets

def handle_tcp_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"TCP Received: {data}")
        client_socket.sendall(b"TCP Response")
    client_socket.close()

def tcp_server():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('0.0.0.0', 5001))
    tcp_socket.listen(5)
    print("TCP Server Listening on port 5001")
    
    while True:
        client_socket, addr = tcp_socket.accept()
        print(f"TCP Connection from {addr}")
        threading.Thread(target=handle_tcp_client, args=(client_socket,)).start()

def udp_server():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 5002))
    print("UDP Server Listening on port 5002")
    
    while True:
        data, addr = udp_socket.recvfrom(1024)
        print(f"UDP Received from {addr}: {data}")
        udp_socket.sendto(b"UDP Response", addr)

async def websocket_handler(websocket, path):
    async for message in websocket:
        print(f"WebSocket Received: {message}")
        await websocket.send("WebSocket Response")

async def websocket_server():
    server = await websockets.serve(websocket_handler, "0.0.0.0", 5003)
    print("WebSocket Server Listening on port 5003")
    await server.wait_closed()
