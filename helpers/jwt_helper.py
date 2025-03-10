from jose import jwt
from datetime import datetime, timedelta, timezone
from config import get_auth_data


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)  # TODO: change token's expire after testing
    to_encode.update({"exp": expire})

    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt
