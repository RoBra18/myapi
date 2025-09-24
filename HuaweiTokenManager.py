import requests
from datetime import datetime, timezone, timedelta
def getNewToken():
    url = "https://iam.ap-southeast-1.myhuaweicloud.com/v3/auth/tokens"
    body = { 
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": "robra137",
                        "password": "Sofivaju4..",  
                        "domain": { "name": "hid_9nboli7-uza9a-d" }
                    }
                }
            },
            "scope": {
                "project": { 
                    "name": "ap-southeast-1",
                    "domain": { "name": "hid_9nboli7-uza9a-d" }
                }
            }
        }
    }

    try:
        response = requests.post(url, json=body, verify=False)
        response.raise_for_status()
        
        # Extraer token del header
        token = response.headers.get("X-Subject-Token")
        if not token:
            raise ValueError("No se encontró el token en los headers")
        
        expires_at = response.json().get("token", {}).get("expires_at")
        if not expires_at:
            raise ValueError("No se encontró 'expires_at' en la respuesta")
        print("Se obtuvieron los datos")
        return (token, expires_at)
    
    except requests.exceptions.RequestException as e:
        print(f"Error de solicitud HTTP: {e}")
        return (0,0)
    except ValueError as ve:
        print(f"Error de extracción: {ve}")
        return (0,0)
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return (0,0)



def is_token_valid(expires_at): 
    try:
        exp_dt = datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        exp_dt = exp_dt.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        return (exp_dt - now) > timedelta(hours=1)
    except Exception as e:
        print(f"Error al procesar expires_at: {e}")
        return False