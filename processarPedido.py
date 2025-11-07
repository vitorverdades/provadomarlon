import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def lambda_handler(event, context):
    
    table_name = os.environ['TABELA_DYNAMO_NOME']
    topic_arn = os.environ['TOPICO_SNS_ARN']
    
    table = dynamodb.Table(table_name)
    
    try:
        for record in event['Records']:
            
            dados = json.loads(record['body'])
            
            dados['status_pedido'] = 'APROVADO'
            
            table.put_item(Item=dados)
            
            print(f"Salvou o pedido {dados['id_pedido']}")
            
            sns.publish(
                TopicArn=topic_arn,
                Message=f"Seu pedido {dados['id_pedido']} foi aprovado!",
                Subject="Status do Pedido"
            )
            
        return {
            'statusCode': 200,
            'body': json.dumps('Pedidos processados.')
        }

    except Exception as e:
        print(f"Falha no processamento: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Erro ao processar a fila.')
        }