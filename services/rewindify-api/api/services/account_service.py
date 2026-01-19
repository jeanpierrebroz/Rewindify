"""Account management service for Rewindify."""

from firebase_admin import auth


async def create_account(token: str):
    decoded_token: dict = auth.verify_id_token(token)
    uid: str = decoded_token["uid"]
    email: str = decoded_token.get("email")

    