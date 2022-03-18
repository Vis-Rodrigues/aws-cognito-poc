from login import login
from refresh_token import refresh_token
from utils.utils import get_body, logger_info


def lambda_handler(event, context):
    route = get_route(event)
    body = get_body(event['body'])

    if route == '/fiap-hmv/v1/login':
        return login(body)
    elif route == '/fiap-hmv/v1/login/refresh-token':
        return refresh_token(body)


def get_route(event):
    resource: str = event.get('resource', None)
    if not resource:
        raise BaseException('The resource key was not found in event.')

    logger_info('Resource: {}'.format(resource))

    return resource
