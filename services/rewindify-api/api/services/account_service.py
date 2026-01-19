"""Account management service for Rewindify."""

from firebase_admin import auth
from shared_db import client


async def create_account(token: str):
    decoded_token: dict = auth.verify_id_token(token)
    uid: str = decoded_token["uid"]
    email: str = decoded_token.get("email")

    # try:
    #     user = 
    #     return user






