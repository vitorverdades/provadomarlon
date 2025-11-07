1. Visão Geral
O sistema é desenhado para desacoplar a submissão do pedido do seu processamento. Isso garante que o cliente receba uma resposta rápida de confirmação, enquanto o processamento mais pesado ocorre em background, aumentando a resiliência e a escalabilidade do sistema.

2. Componentes da Arquitetura
Cliente (Computador): O usuário ou sistema que origina a solicitação de pedido.

Gateway de API (Ícone 'B'): O ponto de entrada (endpoint) que recebe a requisição HTTP do cliente.

AWS Lambda (submeterPedido): Uma função serverless que recebe a requisição do API Gateway. Sua única responsabilidade é validar rapidamente o pedido e enviá-lo para a fila de mensagens.

Amazon MQ (Ícone rosa com setas): Um serviço de broker de mensagens (fila) que armazena o pedido. Ele atua como um buffer, desacoplando a submissão do processamento.

AWS Lambda (processarPedido): Uma função serverless que é acionada quando uma nova mensagem (pedido) chega na fila do Amazon MQ. Esta função contém a lógica de negócio principal para processar o pedido.

Amazon DynamoDB (Ícone de banco de dados): Um banco de dados NoSQL onde a função processarPedido armazena as informações do pedido após o processamento.

Amazon SNS (Ícone rosa com filtro): Um serviço de notificação. Ele é usado para enviar uma notificação de volta ao cliente (ou a um sistema de monitoramento) assim que o pedido é recebido na fila, confirmando a submissão.

3. Fluxo de Dados
O Cliente envia uma requisição de novo pedido (ex: POST /pedido) para o Gateway de API.

O Gateway de API aciona a função Lambda submeterPedido.

A função submeterPedido envia o pedido como uma mensagem para o broker Amazon MQ.

O Amazon MQ realiza duas ações simultaneamente (padrão fan-out):

A) Envia uma mensagem para o tópico Amazon SNS, que por sua vez notifica o Cliente (ex: "Seu pedido foi recebido!").

B) Aciona a função Lambda processarPedido para iniciar o processamento.

A função processarPedido executa a lógica de negócio (verifica estoque, processa pagamento, etc.) e, ao finalizar, salva o pedido processado no banco de dados Amazon DynamoDB.

Posso ajudar a detalhar algum desses serviços ou a escrever o código para uma das funções Lambda?