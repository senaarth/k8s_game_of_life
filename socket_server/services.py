import random
import socket

engine_hosts = {
    "omp": {
        "host": "jogodavida-omp",  # Nome do serviço OMP no Kubernetes ou Docker
        "port": 6000,
    },
    "mpi": {
        "host": "jogodavida-mpi",  # Nome do serviço MPI no Kubernetes ou Docker
        "port": 7000,
    },
    "spark": {
        "host": "jogodavida-spark",  # Nome do serviço Spark no Kubernetes ou Docker
        "port": 8000,
    },
}

def submit_values_to_engines(powmin, powmax):
    chosen_engine = random.choice(["omp", "mpi", "spark"])
    engine_host = engine_hosts[chosen_engine]["host"]
    engine_port = engine_hosts[chosen_engine]["port"]

    print(f"Send to {chosen_engine}, address {engine_host}:{engine_port}, powmin {powmin} and powmax {powmax}")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((engine_host, engine_port))
            
            message = f"{powmin},{powmax}".encode()
            s.sendall(message)
            
            response = s.recv(1024).decode()

            print(f"Received response from {chosen_engine}: {response}")
            return response
    except Exception as e:
        print(f"Error connecting to {chosen_engine}: {e}")
        return f"Erro {e}"
