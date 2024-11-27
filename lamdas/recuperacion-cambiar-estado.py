import json
import pymysql
import boto3
import threading

# Configuración de conexión a RDS
RDS_HOST = 'salon-citas.coxkquhymmdl.us-east-1.rds.amazonaws.com'
RDS_USER = 'admin'
RDS_PASSWORD = 'Guitarra99.'
RDS_DATABASE = 'salon_citas'

# Configuración de la Lambda que enviará a la cola
LAMBDA_CLIENT = boto3.client('lambda')
ENVIAR_COLA_FUNCTION_NAME = 'recuperacion-notificacion-cola-sender'  # Nombre de la Lambda que envía mensajes a la cola


def lambda_handler(event, context):
    try:
        # Depuración: imprime el evento completo
        print("Evento recibido:", event)

        # Decodificar el cuerpo si es una cadena
        if isinstance(event.get('body'), str):
            try:
                body = json.loads(event['body'])
            except json.JSONDecodeError:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": "El cuerpo de la solicitud no es un JSON válido",
                        "raw_body": event['body']
                    })
                }
        else:
            body = event.get('body', {})

        # Extraer datos del cuerpo
        cita_id = body.get('cita_id')
        nuevo_estado = body.get('estado')

        print(f"Datos extraídos - cita_id: {cita_id}, estado: {nuevo_estado}")

        if not cita_id or not nuevo_estado:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Se requiere cita_id y estado",
                    "input_received": body
                })
            }

        # Validar que el estado sea permitido
        estados_permitidos = ['completada', 'cancelada']
        if nuevo_estado not in estados_permitidos:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"Estado no permitido. Debe ser uno de {estados_permitidos}",
                    "estado_recibido": nuevo_estado
                })
            }

        # Conectar a RDS
        print("Conectando a la base de datos...")
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DATABASE
        )
        print("Conexión a la base de datos establecida.")

        try:
            with connection.cursor() as cursor:
                # Actualizar el estado de la cita
                print(f"Actualizando cita con ID {cita_id} al estado {nuevo_estado}")
                query = "UPDATE citas SET estado = %s WHERE id = %s"
                cursor.execute(query, (nuevo_estado, cita_id))
                connection.commit()

                # Verificar si se actualizó alguna fila
                if cursor.rowcount == 0:
                    print(f"No se encontró ninguna cita con ID {cita_id}")
                    return {
                        "statusCode": 404,
                        "body": json.dumps({
                            "message": "Cita no encontrada",
                            "cita_id": cita_id
                        })
                    }

                print(f"Estado de la cita con ID {cita_id} actualizado exitosamente a {nuevo_estado}")

                # Llamar a la Lambda que envía el mensaje a la cola si el estado es "cancelada"
                if nuevo_estado == 'cancelada':
                    
                    # Llamar a la Lambda que consulta el rol en RDS
                    lambda_response = LAMBDA_CLIENT.invoke(
                        FunctionName='recuperacion-notificacion-cola-sender',  # Cambia esto por el nombre real de la Lambda
                        InvocationType='RequestResponse',
                        Payload=json.dumps({"cita_id": cita_id})
                    )
                    
                    print(f"Respuesta de la Lambda de enviar a la cola: {lambda_response}")
                

                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "Estado de la cita actualizado con éxito",
                        "cita_id": cita_id,
                        "nuevo_estado": nuevo_estado
                    })
                }

        finally:
            connection.close()
            print("Conexión a la base de datos cerrada.")

    except Exception as e:
        # Depuración: registrar la excepción
        print("Error inesperado:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"Error al actualizar el estado de la cita: {str(e)}",
                "input_received": event
            })
        }
