import socket
import time
import numpy as np
from pyspark.sql import SparkSession

def ind2d(i, j, tam):
    return i * (tam + 2) + j

def uma_vida(tabul_in, tabul_out, tam):
    for i in range(1, tam+1):
        for j in range(1, tam+1):
            vizviv = (
                tabul_in[ind2d(i-1, j-1, tam)] + tabul_in[ind2d(i-1, j, tam)] +
                tabul_in[ind2d(i-1, j+1, tam)] + tabul_in[ind2d(i, j-1, tam)] +
                tabul_in[ind2d(i, j+1, tam)] + tabul_in[ind2d(i+1, j-1, tam)] +
                tabul_in[ind2d(i+1, j, tam)] + tabul_in[ind2d(i+1, j+1, tam)]
            )
            if tabul_in[ind2d(i, j, tam)] and vizviv < 2:
                tabul_out[ind2d(i, j, tam)] = 0
            elif tabul_in[ind2d(i, j, tam)] and vizviv > 3:
                tabul_out[ind2d(i, j, tam)] = 0
            elif not tabul_in[ind2d(i, j, tam)] and vizviv == 3:
                tabul_out[ind2d(i, j, tam)] = 1
            else:
                tabul_out[ind2d(i, j, tam)] = tabul_in[ind2d(i, j, tam)]

def init_tabul(tabul_in, tabul_out, tam):
    tabul_in.fill(0)
    tabul_out.fill(0)
    tabul_in[ind2d(1, 2, tam)] = 1
    tabul_in[ind2d(2, 3, tam)] = 1
    tabul_in[ind2d(3, 1, tam)] = 1
    tabul_in[ind2d(3, 2, tam)] = 1
    tabul_in[ind2d(3, 3, tam)] = 1

def correto(tabul, tam):
    return (
        np.sum(tabul) == 5 and
        tabul[ind2d(tam-2, tam-1, tam)] and
        tabul[ind2d(tam-1, tam, tam)] and
        tabul[ind2d(tam, tam-2, tam)] and
        tabul[ind2d(tam, tam-1, tam)] and
        tabul[ind2d(tam, tam, tam)]
    )

def main():
    spark = SparkSession.builder \
        .appName("GameOfLife") \
        .config("spark.executor.extraJavaOptions", "--add-opens java.base/java.nio=ALL-UNNAMED") \
        .config("spark.driver.extraJavaOptions", "--add-opens java.base/java.nio=ALL-UNNAMED") \
        .getOrCreate()
    
    # TCP server setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 30007))
    server_socket.listen(1)
    
    print("Aguardando conexão na porta 30007...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão recebida de {addr}")
        
        data = client_socket.recv(1024).decode()

        if data.strip().lower() == "exit":  # Adiciona a condição de saída
            print("Comando de saída recebido. Encerrando servidor.")
            client_socket.send(b"Servidor encerrando...\n")
            client_socket.close()
            break  # Sai do loop, permitindo que o Spark seja encerrado

        try:
            powmin, powmax = map(int, data.split())
        except ValueError:
            client_socket.send(b"Erro: POWMIN e POWMAX devem ser inteiros validos.\n")
            client_socket.close()
            continue

        if powmin <= 0 or powmax <= 0 or powmin > powmax:
            client_socket.send(b"Erro: POWMIN e POWMAX devem ser inteiros positivos e POWMIN <= POWMAX\n")
            client_socket.close()
            continue

        for pow in range(powmin, powmax + 1):
            tam = 1 << pow
            tabul_in = np.zeros((tam+2)*(tam+2), dtype=int)
            tabul_out = np.zeros((tam+2)*(tam+2), dtype=int)
            
            t0 = time.time()
            init_tabul(tabul_in, tabul_out, tam)
            t1 = time.time()

            for _ in range(2 * (tam - 3)):
                uma_vida(tabul_in, tabul_out, tam)
                uma_vida(tabul_out, tabul_in, tam)

            t2 = time.time()

            if correto(tabul_in, tam):
                result = "**Ok, RESULTADO CORRETO**"
            else:
                result = "**Nok, RESULTADO ERRADO**"

            print(result)

            t3 = time.time()

            response = f"tam={tam},init={t1-t0:.7f},comp={t2-t1:.7f},fim={t3-t2:.7f},tot={t3-t0:.7f} \n"
            client_socket.send(response.encode())

        client_socket.close()

    server_socket.close()
    spark.stop()

if __name__ == "__main__":
    main()
