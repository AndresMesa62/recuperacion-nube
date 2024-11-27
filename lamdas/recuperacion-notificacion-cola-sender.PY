import json
import boto3

# Configuración de SQS
SQS_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/144270817558/cola-cancelacion'

def lambda_handler(event, context):
    try:
        # Crear el cliente de SQS
        sqs = boto3.client('sqs')
        
        # Log de depuración del evento recibido
        print("=== INICIO DE LAMBDA ===")
        print("Evento recibido completo:", json.dumps(event, indent=4))

        # Extraer datos del evento
        cita_id = event.get('cita_id')
        accion = 'cancelacion'  # Por defecto, usamos "cancelacion"

        print(f"Datos extraídos - cita_id: {cita_id}, accion: {accion}")

        if not cita_id:
            print("Error: 'cita_id' no encontrado en el evento.")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Se requiere cita_id",
                    "input_received": event
                })
            }

        # Crear el mensaje para enviar a la cola
        message = {
            "cita_id": cita_id,
            "accion": accion
        }
        
        print("Mensaje que se enviará a SQS:", json.dumps(message, indent=4))

        # Enviar el mensaje a la cola
        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(message)
        )
        
        print("Respuesta de SQS:", json.dumps(response, indent=4))

        print("=== FIN DE LAMBDA ===")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Mensaje enviado a la cola SQS con éxito",
                "messageId": response.get('MessageId'),
                "input_received": event
            })
        }
    except Exception as e:
        # Log de error detallado
        print("Error al enviar el mensaje a SQS:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"Error al enviar el mensaje: {str(e)}",
                "input_received": event
            })
        }
