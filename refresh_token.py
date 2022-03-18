import os
import boto3
import jwt
from utils.utils import get_secret_hash, return_response, logger_info, logger_error


def decode_access_token(event):
    access_token = event['access_token']
    decoded = jwt.decode(access_token, options={"verify_signature": False})
    logger_info(decoded)
    decoded_username = decoded["username"]
    return decoded_username


def refresh_token(event):
    client = boto3.client('cognito-idp')

    try:

        username = decode_access_token(event)

        response = client.initiate_auth(
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': event['refresh_token'],
                'SECRET_HASH': get_secret_hash(username)

                # 'REFRESH_TOKEN': event['refresh_token'], 'SECRET_HASH': get_secret_hash(event['username']) #when
                # you have an “@” in the username you get that error on the REFRESH_TOKEN_AUTH call. Cognito
                # generates a UUID-style username for them. And you have to use that during the refresh call.
            },
            ClientId=os.environ['clientId']
        )

        logger_info('Token updated successfully.')

        return return_response(201, 'Token atualizado com sucesso.', response)

    except client.exceptions.NotAuthorizedException as e:
        logger_error(str(e))
        return return_response(422, 'As credenciais do token de atualização não correspondem. ')

    except Exception as e:
        logger_error(str(e))
        return return_response(500, "Algo deu errado, tente novamente")
