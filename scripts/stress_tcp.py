import sys
import socket
import threading
import time

def send_socket_message(ip, port, message, duration):
    start_time = time.time()
    while True:
        try:
            if time.time() - start_time > duration:
                print("Tempo de execução atingido, encerrando thread.")
                break
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))
                sock.sendall(message.encode())
                response = sock.recv(1024)
                print(f"Recebido: {response.decode()}")
        except Exception as e:
            print(f"Erro: {e}")
            break

if __name__ == "__main__":
    # exemplo de uso python stress_tcp.py 5 omp,3,5 10
    threads_num = int(sys.argv[1])
    message = sys.argv[2]
    duration = int(sys.argv[3])  # Duração do teste em segundos

    print(f"Starting {threads_num} threads for {duration} seconds...")

    for i in range(threads_num):
        thread = threading.Thread(target=send_socket_message, args=("104.154.205.216", 30001, message, duration))
        thread.start()
