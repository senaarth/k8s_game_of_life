import random

engine_hosts = {
    "omp": {
        "host": "jogodavida_omp",
        "port": 6000,
    },
    "mpi": {
        "host": "jogodavida_mpi",
        "port": 7000,
    },
    "spark": {
        "host": "jogodavida_spark",
        "port": 8000,
    },
}

def submit_values_to_engines(powmin, powmax):
    chosen_engine = random.choice(["omp", "mpi", "spark"])
    engine_host = engine_hosts[chosen_engine]["host"]
    engine_port = engine_hosts[chosen_engine]["port"]

    print(f"Send to {chosen_engine}, address {engine_host}:{engine_port}, powmin {powmin} and powmax {powmax}")

    return "Engine response"
