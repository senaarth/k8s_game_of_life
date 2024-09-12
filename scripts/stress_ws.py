import sys
import asyncio
from playwright.async_api import async_playwright
import random
import time

# Definindo uma URI fixa para o WebSocket
URI = "ws://104.154.205.216:30003"

async def stress_test(engine, powmin, powmax, num_threads, duration):
    async def run_client(client_id):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Adicionando o comportamento real do cliente WebSocket
            await page.evaluate(f"""
                window.isConnectedToServer = false;

                const socket = new WebSocket('{URI}');
                
                socket.onopen = function(event) {{
                    window.isConnectedToServer = true;
                    console.log('Client {client_id}: Conectado ao servidor WebSocket.');
                }};
                
                socket.onmessage = function(event) {{
                    console.log('Client {client_id}: Resposta do servidor: ', event.data);
                }};
                
                socket.onerror = function(error) {{
                    console.error('Client {client_id}: Erro no WebSocket: ', error);
                }};
                
                socket.onclose = function(event) {{
                    window.isConnectedToServer = false;
                    console.log('Client {client_id}: Conexão com o servidor WebSocket fechada.');
                }};

                // Função para enviar requisição
                window.submitRequest = function(engine, powmin, powmax) {{
                    if (window.isConnectedToServer && socket.readyState === WebSocket.OPEN) {{
                        const message = JSON.stringify({{ engine, powmin, powmax }});
                        socket.send(message);
                        console.log('Client {client_id}: Mensagem enviada:', message);
                    }} else {{
                        console.error('Client {client_id}: Não conectado ao servidor.');
                    }}
                }};
            """)

            # Aguarda a conexão WebSocket estar aberta
            await page.wait_for_function("window.isConnectedToServer === true", timeout=10000)
            print(f"Client {client_id}: WebSocket connection opened")

            start_time = time.time()

            # Simula envios de mensagens usando submitRequest
            while time.time() - start_time < duration:
                # Envia a mensagem JSON via WebSocket
                await page.evaluate(f"window.submitRequest('{engine}', {powmin}, {powmax});")

                # Aguarda um curto período de tempo antes de enviar outra mensagem
                await asyncio.sleep(random.uniform(0.5, 1.0))  # Simula latência entre mensagens

            # Aguarda por um curto período para garantir que todas as mensagens foram processadas
            await asyncio.sleep(2)
            await browser.close()
            print(f"Client {client_id}: Browser closed")

    # Cria múltiplas tarefas para simular múltiplos clientes
    tasks = [run_client(i) for i in range(num_threads)]
    await asyncio.gather(*tasks)

def main():
    if len(sys.argv) < 5:
        print("Usage: python stress_ws.py <engine> <threads> <duration> <powmin> <powmax>")
        sys.exit(1)

    engine = sys.argv[1]
    num_threads = int(sys.argv[2])
    duration = int(sys.argv[3])
    powmin = int(sys.argv[4])
    powmax = int(sys.argv[5])

    print(f"Starting stress test with engine {engine}, {num_threads} threads, duration {duration}s, "
          f"powmin {powmin}, powmax {powmax}")
    
    # Executa o teste de stress
    asyncio.run(stress_test(engine, powmin, powmax, num_threads, duration))

if __name__ == "__main__":
    main()
