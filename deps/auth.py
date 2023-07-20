import jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from decouple import config

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret = config('JWT_SECRET')


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def encode_token(user_id: int, restaurant_id: int):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0, hours=6),
        'iat': datetime.utcnow(),
        'sub': user_id,
        'restaurant_id': restaurant_id
    }
    return jwt.encode(
        payload,
        secret,
        algorithm='HS256'
    )


def decode_token(token: str):
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Signature has expired')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Invalid token')


def current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return decode_token(token)
