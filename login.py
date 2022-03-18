import boto3
import os
import hmac
import hashlib
import base64
from refresh_token import refresh_token


# def decode_access_token(event):
#     accessToken = event['access_token']
#     decoded = jwt.decode(accessToken, options={"verify_signature": False})
#     print(decoded)
#     decodedUsername = decoded["username"]
#     return decodedUsername


def get_secret_hash(username):
    msg = username + os.environ['clientId']
    dig = hmac.new(str(os.environ['clientSecret']).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def returnResponse(code, message, data=None):
    return {
        'statusCode': code,
        'body': {
            'message': message,
            'data': data
        }
    }


def lambda_handler(event, context):
    print(event)
    if event['type'] == 'login':
        login(event)
    else:
        refresh_token(event)


def login(event):
    client = boto3.client('cognito-idp')

    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': event['email'],
                'PASSWORD': event['password'],
                'SECRET_HASH': get_secret_hash(event['email']),
            },
            ClientMetadata={
                'username': event['email'],
                'password': event['password']
            },
            ClientId=os.environ['clientId']
        )

        print(response)

        return returnResponse(200, 'Login realizado com sucesso.', response)

    except client.exceptions.NotAuthorizedException as e:
        print(str(e))
        return returnResponse(422, 'As credenciais não correspondem.')

    except client.exceptions.PasswordResetRequiredException as e:
        print(str(e))
        return returnResponse(422, 'É necessario resetar a sua senha.')

    except client.exceptions.UserNotConfirmedException as e:
        print(str(e))
        return returnResponse(422, 'Usuario ainda não confirmado.')

    except Exception as e:
        print(str(e))
        return returnResponse(500, "Algo deu errado. Por favor, tente novamente mais tarde ")

# def refresh_token(event):
#     client = boto3.client('cognito-idp')

#     try:

#         username = decode_access_token(event)

#         response = client.initiate_auth(
#             AuthFlow='REFRESH_TOKEN_AUTH',
#             AuthParameters={
#                 'REFRESH_TOKEN': event['refresh_token'],
#                 'SECRET_HASH': get_secret_hash(username)

#                 # 'REFRESH_TOKEN': event['refresh_token'], 'SECRET_HASH': get_secret_hash(event['username']) #when
#                 # you have an “@” in the username you get that error on the REFRESH_TOKEN_AUTH call. Cognito
#                 # generates a UUID-style username for them. And you have to use that during the refresh call.
#             },
#             ClientId=os.environ['clientId']
#         )

#         print(response)

#         return returnResponse(200, 'Token atualizado com sucesso.', response)

#     except client.exceptions.NotAuthorizedException as e:
#         print(str(e))
#         return returnResponse(422, 'As credenciais do token de atualização não correspondem. ')

#     except Exception as e:
#         print(str(e))
#         return returnResponse(500, "Algo deu errado, tente novamente")