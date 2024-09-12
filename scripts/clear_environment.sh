#!/bin/bash

# Lista de pastas e as respectivas imagens Docker no Google Container Registry (GCR)
folders=(
    "mpi" 
    "omp" 
    "spark"
    "pyspark" 
    "socket_server" 
    "client" 
    "database"
)

# Função para deletar os YAMLs no Kubernetes
delete_yml() {
    local dir=$1
    
    echo "Entrando na pasta $dir"
    cd "$dir" || exit
    
    echo "Deletando os arquivos YAML/YML no Kubernetes..."
    for yaml_file in ./*.yml; do
        if [ -f "$yaml_file" ]; then
            kubectl delete -f "$yaml_file"
        else
            echo "Nenhum arquivo YAML ou YML encontrado na pasta $dir"
        fi
    done

    echo "Saindo da pasta $dir"
    cd - || exit
}

# Vai pra raiz
cd '../' || exit

# Itera sobre os serviços e deleta os YAMLs
for i in "${!folders[@]}"; do
    delete_yml "${folders[$i]}"
done

kubectl delete -f https://github.com/cert-manager/cert-manager/releases/download/v1.9.1/cert-manager.yaml
kubectl delete -f https://download.elastic.co/downloads/eck/2.9.0/crds.yaml
kubectl delete -f https://download.elastic.co/downloads/eck/2.9.0/operator.yaml

echo "Processo de deleção concluído!"
