import json
import boto3
import os

# Configuración de SQS
SQS_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/144270817558/cola-cancelacion'
sqs_client = boto3.client('sqs')

# Configuración de SES
ses_client = boto3.client('ses', region_name='us-east-1')
FROM_EMAIL = 'sistemas@indeccaldas.gov.co'
TO_EMAIL = 'sistemas@indeccaldas.gov.co'

def lambda_handler(event, context):
    try:
        # Obtener mensajes de la cola
        messages = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1
        )

        if 'Messages' not in messages:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "No hay mensajes en la cola"})
            }

        for message in messages['Messages']:
            message_body = json.loads(message['Body'])
            cita_id = message_body.get('cita_id')
            accion = message_body.get('accion')

            if not cita_id or not accion:
                print("Mensaje incompleto:", message_body)
                continue

            # Preparar el cuerpo del correo
            email_body = f"""
            <html>
                <body>
                    <h2>Cita Cancelada</h2>
                    <p>Se ha cancelado la cita con ID: <strong>{cita_id}</strong>.</p>
                </body>
            </html>
            """

            try:
                # Enviar correo con SES
                ses_client.send_email(
                    Source=FROM_EMAIL,
                    Destination={
                        'ToAddresses': [TO_EMAIL]
                    },
                    Message={
                        'Subject': {
                            'Data': 'Notificación de Cancelación de Cita'
                        },
                        'Body': {
                            'Html': {
                                'Data': email_body
                            }
                        }
                    }
                )

                # Eliminar el mensaje procesado de la cola
                sqs_client.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                )
                print(f"Mensaje eliminado: {message['MessageId']}")

            except Exception as e:
                print(f"Error al enviar correo a {TO_EMAIL}: {e}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Mensajes procesados correctamente"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error al procesar los mensajes: {str(e)}"})
        }
