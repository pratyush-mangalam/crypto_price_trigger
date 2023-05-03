from datetime import datetime, timedelta

from django.conf import settings

import jwt

from crypto_price_trigger.utils.custom_exception import InvalidTokenException


def generate_jwt_token(user):
    """
    The generate_jwt_token function takes in a user object and returns a JWT token.
    The payload of the token contains the user's id, email, expiration time (60 minutes), and issue time.

    :param user: Generate a jwt token
    :return: A token that is encoded with the user's id, email and a secret key
    """
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "exp": datetime.utcnow() + timedelta(minutes=60),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    return token


def decode_jwt_token(token):
    """
    The decode_jwt_token function takes a token as an argument and returns the payload of that token.
    The function first removes the 'Bearer ' prefix from the token, then decodes it using jwt.decode().
    If there is an error decoding, it raises either InvalidTokenException or ExpiredSignatureError.

    :param token: Decode the token
    :return: The payload of the token
    """
    try:
        token = token[7:]
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise InvalidTokenException("Token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenException("Invalid token")


def refresh_jwt_token(token):
    """
    The refresh_jwt_token function takes in a token and returns a new token.
        It decodes the old token, checks if it is valid, then creates a new payload with the same user_id and email as before.
        The expiry time of this new payload is set to 15 minutes from now (the default).
        This function will be used when we want to refresh an expired JWT.

    :param token: Decode the token and get the user_id and email from it
    :return: A new token
    """
    payload = decode_jwt_token(token)
    if isinstance(payload, str):
        return payload
    user_id = payload["user_id"]
    email = payload["email"]
    new_payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "iat": datetime.utcnow(),
    }
    new_token = jwt.encode(
        new_payload, settings.JWT_SECRET_KEY, algorithm="HS256"
    )
    return new_token.decode("utf-8")
