#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 6001
#define BUFFER_SIZE 1024

int main()
{
  int server_fd, new_socket;
  struct sockaddr_in address;
  int addrlen = sizeof(address);
  char buffer[BUFFER_SIZE] = {0};
  const char *confirmation_message = "Dados recebidos com sucesso!\n";

  // Criando o socket
  if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
  {
    perror("Falha ao criar socket");
    exit(EXIT_FAILURE);
  }

  // Definindo as opções de socket
  address.sin_family = AF_INET;
  address.sin_addr.s_addr = INADDR_ANY;
  address.sin_port = htons(PORT);

  // Ligando o socket à porta 600
  if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
  {
    perror("Falha ao fazer bind");
    exit(EXIT_FAILURE);
  }

  // Colocando o socket em modo de escuta
  if (listen(server_fd, 3) < 0)
  {
    perror("Falha ao escutar");
    exit(EXIT_FAILURE);
  }

  printf("Aguardando conexões na porta %d...\n", PORT);

  while (1)
  {
    // Aceitando uma conexão
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0)
    {
      perror("Falha ao aceitar conexão");
      exit(EXIT_FAILURE);
    }

    // Limpando o buffer
    memset(buffer, 0, BUFFER_SIZE);

    // Recebendo o valor via TCP
    int valread = read(new_socket, buffer, BUFFER_SIZE);
    if (valread > 0)
    {
      printf("Valor recebido: %s\n", buffer);

      // Enviar confirmação de recebimento ao cliente
      write(new_socket, confirmation_message, strlen(confirmation_message));
    }
    else
    {
      printf("Conexão encerrada pelo cliente.\n");
    }

    // Fechando o socket de cliente
    close(new_socket);
  }

  // Fechando o socket do servidor
  close(server_fd);

  return 0;
}