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
        email = event.get('email')
        fecha_cita = event.get('fecha_cita')
        
        if not email or not fecha_cita:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Se requiere email y fecha_cita"})
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
                # Obtener el usuario_id basado en el email
                query_usuario = "SELECT id FROM usuarios WHERE email = %s"
                cursor.execute(query_usuario, (email,))
                result = cursor.fetchone()
                
                if not result:
                    return {
                        "statusCode": 404,
                        "body": json.dumps({"message": "Usuario no encontrado"})
                    }
                
                usuario_id = result[0]
                
                # Insertar la nueva cita en la tabla
                query_cita = """
                INSERT INTO citas (usuario_id, fecha_cita, estado)
                VALUES (%s, %s, 'activa')
                """
                cursor.execute(query_cita, (usuario_id, fecha_cita))
                connection.commit()
                
                return {
                    "statusCode": 201,
                    "body": json.dumps({"message": "Cita creada exitosamente"})
                }
        
        finally:
            connection.close()
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error al agendar la cita: {str(e)}"})
        }
