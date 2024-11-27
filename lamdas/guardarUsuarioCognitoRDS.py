import pymysql
import os

# Configuración de conexión a RDS
RDS_HOST = 'salon-citas.coxkquhymmdl.us-east-1.rds.amazonaws.com'
RDS_USER = 'admin'
RDS_PASSWORD = 'Guitarra99.'
RDS_DATABASE = 'salon_citas'

def lambda_handler(event, context):
    # Extraer datos del evento
    cognito_user_id = event['userName']
    user_attributes = event['request']['userAttributes']
    nombre = user_attributes.get('name', 'No Name')
    email = user_attributes.get('email', None)
    tipo = 'default'

    if not email:
        # Cognito no espera este formato de respuesta; lanza una excepción si hay un error
        raise ValueError("El usuario no tiene un correo electrónico válido.")

    # Conectar a RDS
    connection = pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DATABASE
    )
    
    try:
        with connection.cursor() as cursor:
            # Verificar si el usuario ya existe
            query = "SELECT id FROM usuarios WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            
            if result:
                # Si el usuario ya existe, actualiza su último inicio de sesión
                update_query = """
                UPDATE usuarios
                SET ultimo_login = NOW()
                WHERE email = %s
                """
                cursor.execute(update_query, (email,))
            else:
                # Si el usuario no existe, lo crea
                insert_query = """
                INSERT INTO usuarios (cognito_user_id, nombre, email, ultimo_login, tipo)
                VALUES (%s, %s, %s, NOW(), %s)
                """
                cursor.execute(insert_query, (cognito_user_id, nombre, email, tipo))
            
            connection.commit()
    finally:
        connection.close()
    
    return event
