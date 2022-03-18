import os
import hmac
import hashlib
import base64
import json
import logging

logging.getLogger().setLevel(logging.INFO)


def get_secret_hash(username):
    msg = username + get_environ('client_id')
    dig = hmac.new(str(get_environ('client_secret')).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def return_response(code, message, data=None):
    return {
        "statusCode": code,
        "body": json.dumps({
            'message': message,
            'data': data
        })
    }


def get_environ(name_env):
    return os.environ[name_env]


def get_body(request):
    return json.loads(request)


def logger_info(message):
    logging.info(message)


def logger_error(message):
    logging.error(message)