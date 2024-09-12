FROM apache/spark:v3.4.0

# Instalar Python e pip
USER root
RUN apt-get update && apt-get install -y python3 python3-pip

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos para o contêiner
COPY . /app

# Instalar dependências Python
RUN pip3 install numpy pyspark

# Expor a porta TCP 30007
EXPOSE 30007

# Comando para executar o servidor TCP
CMD ["python3", "jogodavida_spark.py"]
