import jwt
import datetime



import dotenv
from os import getenv
dotenv.load_dotenv()
env = getenv("JWT_SECRET")

def create_access_token(user_id):
    payload = {
        "sub": str(user_id),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, env, algorithm="HS256")

def decode_access_token(token):
    return jwt.decode(token, env, algorithms="HS256")