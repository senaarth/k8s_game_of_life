#!/bin/bash

# Lista de pastas e as respectivas imagens Docker no Google Container Registry (GCR)
services=("mpi" "omp" "pyspark" "socket_server" "client")
images=(
    "gcr.io/massive-hub-431500-n1/jogodavida-mpi:latest"
    "gcr.io/massive-hub-431500-n1/jogodavida-omp:latest"
    "gcr.io/massive-hub-431500-n1/jogodavida-pyspark:latest"
    "gcr.io/massive-hub-431500-n1/socket-server:latest"
    "gcr.io/massive-hub-431500-n1/client:latest"
)

# Função para buildar, fazer push e aplicar os YAMLs
build_and_deploy() {
    local dir=$1
    local image=$2
    
    echo "Entrando na pasta $dir"
    cd "$dir" || exit
    
    echo "Buildando a imagem Docker $image..."
    docker build --platform linux/amd64 -t "$image" .
    
    echo "Fazendo push da imagem..."
    docker push "$image"
    
    echo "Aplicando os arquivos YAML/YML no Kubernetes..."
    for yaml_file in ./*.yml; do
        if [ -f "$yaml_file" ]; then
            kubectl apply -f "$yaml_file"
        else
            echo "Nenhum arquivo YAML ou YML encontrado na pasta $dir"
        fi
    done

    echo "Saindo da pasta $dir"
    cd - || exit
}

# Função para apenas aplicar os YAMLs (ElasticSearch, Kibana e Metricbeat)
apply_yml_only() {
    local dir=$1
    
    echo "Entrando na pasta $dir"
    cd "$dir" || exit
    
    echo "Aplicando os arquivos YAML/YML no Kubernetes..."
    kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.9.1/cert-manager.yaml
    kubectl apply -f https://download.elastic.co/downloads/eck/2.9.0/crds.yaml
    kubectl apply -f https://download.elastic.co/downloads/eck/2.9.0/operator.yaml
    kubectl apply -f elastic_search.yml
    kubectl apply -f kibana.yml
    # kubectl apply -f metricbeat.yml

    echo "Saindo da pasta $dir"
    cd - || exit
}

# Vai pra raiz
cd - || exit

# Aplicar apenas YAMLs do elastic search
apply_yml_only "database"

kubectl create namespace ingress-nginx

# Itera sobre os serviços e executa o processo de build e deploy
for i in "${!services[@]}"; do
    build_and_deploy "${services[$i]}" "${images[$i]}"
done

echo "Processo concluído!"
