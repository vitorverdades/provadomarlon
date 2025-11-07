import json
import boto3
import os 

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    
    try:
        queue_url = os.environ['FILA_PEDIDOS_URL']
        
        data = json.loads(event['body'])
        
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(data)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensagem': 'Pedido recebido e enfileirado!',
                'dados': data
            })
        }

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'mensagem': 'Erro ao processar o pedido.'})
        }