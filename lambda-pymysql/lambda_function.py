import json
import pymysql

# Configuración de conexión a RDS
RDS_HOST = 'salon-citas.coxkquhymmdl.us-east-1.rds.amazonaws.com'
RDS_USER = 'admin'
RDS_PASSWORD = 'Guitarra99.'
RDS_DATABASE = 'salon_citas'

def lambda_handler(event, context):
    try:
        # Extraer datos del evento
        cita_id = event.get('cita_id')
        nuevo_estado = event.get('estado')

        if not cita_id or not nuevo_estado:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Se requiere cita_id y estado"})
            }

        # Validar que el estado sea permitido
        estados_permitidos = ['completada', 'cancelada']
        if nuevo_estado not in estados_permitidos:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": f"Estado no permitido. Debe ser uno de {estados_permitidos}"})
            }

        # Conectar a RDS
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DATABASE
        )

        try:
            with connection.cursor() as cursor:
                # Actualizar el estado de la cita
                query = "UPDATE citas SET estado = %s WHERE id = %s"
                cursor.execute(query, (nuevo_estado, cita_id))
                connection.commit()

                # Verificar si se actualizó alguna fila
                if cursor.rowcount == 0:
                    return {
                        "statusCode": 404,
                        "body": json.dumps({"message": "Cita no encontrada"})
                    }

                return {
                    "statusCode": 200,
                    "body": json.dumps({"message": "Estado de la cita actualizado con éxito"})
                }

        finally:
            connection.close()

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error al actualizar el estado de la cita: {str(e)}"})
        }
