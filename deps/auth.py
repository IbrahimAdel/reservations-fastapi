import jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from decouple import config

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token_secret = config('JWT_SECRET')
refresh_token_secret = config('JWT_REFRESH_SECRET')


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def encode_access_token(user_id: int, restaurant_id: int):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0, hours=6),
        'iat': datetime.utcnow(),
        'sub': user_id,
        'restaurant_id': restaurant_id
    }
    return jwt.encode(
        payload,
        access_token_secret,
        algorithm='HS256'
    )


def encode_refresh_token(user_id: int, restaurant_id: int):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=2),
        'iat': datetime.utcnow(),
        'sub': user_id,
        'restaurant_id': restaurant_id
    }
    return jwt.encode(
        payload,
        refresh_token_secret,
        algorithm='HS256'
    )


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, access_token_secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Signature has expired')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Invalid token')


def current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return decode_access_token(token)


def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, refresh_token_secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Signature has expired')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Invalid token')
