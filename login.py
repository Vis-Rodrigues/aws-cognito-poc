import boto3
import os
from utils.utils import get_secret_hash, return_response, logger_info, logger_error


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

        logger_info('Login successfully for user {}.'.format(event['email']))

        return return_response(201, 'Login realizado com sucesso.', response)

    except client.exceptions.NotAuthorizedException as e:
        logger_error(str(e))
        return return_response(422, 'As credenciais não correspondem.')

    except client.exceptions.PasswordResetRequiredException as e:
        logger_error(str(e))
        return return_response(422, 'É necessario resetar a sua senha.')

    except client.exceptions.UserNotConfirmedException as e:
        logger_error(str(e))
        return return_response(422, 'Usuario ainda não confirmado.')

    except Exception as e:
        logger_error(str(e))
        return return_response(500, "Algo deu errado. Por favor, tente novamente mais tarde ")

