import json
import requests
import boto3

# Configuración de Cognito
COGNITO_DOMAIN = "https://us-east-1wvajz8fth.auth.us-east-1.amazoncognito.com"

# Configuración del cliente Lambda
LAMBDA_CLIENT = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        # Obtener el access_token del evento
        access_token = event.get("access_token")
        if not access_token:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "No se recibió el access_token"})
            }
        
        # Endpoint de userInfo para verificar el token
        user_info_endpoint = f"{COGNITO_DOMAIN}/oauth2/userInfo"
        
        # Enviar el token para validación
        response = requests.get(
            user_info_endpoint,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        # Analizar la respuesta
        if response.status_code == 200:
            user_info = response.json()
            email = user_info.get("email")
            
            if not email:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"message": "No se pudo extraer el correo del token"})
                }
            
            # Llamar a la Lambda que consulta el rol en RDS
            lambda_response = LAMBDA_CLIENT.invoke(
                FunctionName='recuperacion_consulta_rol',
                InvocationType='RequestResponse',
                Payload=json.dumps({"email": email})
            )
            
            # Procesar la respuesta de la Lambda
            response_payload = json.loads(lambda_response['Payload'].read())
            if response_payload.get("statusCode") != 200:
                return {
                    "statusCode": response_payload.get("statusCode", 500),
                    "body": response_payload.get("body", "{}")
                }
            
            # Combinar los datos del token y el rol
            user_info["tipo"] = json.loads(response_payload["body"]).get("tipo", "default")
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Validación exitosa",
                    "user_info": user_info
                })
            }
        else:
            return {
                "statusCode": 401,
                "body": json.dumps({
                    "message": "Token inválido",
                    "error": response.json()
                })
            }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error durante la validación: {str(e)}"})
        }
