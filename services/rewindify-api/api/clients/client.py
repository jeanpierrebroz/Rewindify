from dotenv import load_dotenv
import os
import base64
import urllib.parse
import requests

# =======================
# CONFIG
# =======================
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"

# auth code fetched once when setting up
AUTH_CODE = os.getenv("SPOTIFY_AUTH_CODE")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")


# =======================
# SETUP
# =======================

# def get_auth_url(client_id, redirect_uri):

#     scope = "user-read-recently-played"
#     params = {
#         "response_type": "code",
#         "client_id": client_id,
#         "redirect_uri": redirect_uri,
#         "scope": scope,
#     }
#     return "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)


# def exchange_code_for_tokens(auth_code, client_id, client_secret, redirect_uri):
#     auth_b64 = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

#     resp = requests.post(
#         "https://accounts.spotify.com/api/token",
#         headers={
#             "Authorization": f"Basic {auth_b64}",
#             "Content-Type": "application/x-www-form-urlencoded",
#         },
#         data={
#             "grant_type": "authorization_code",
#             "code": auth_code,
#             "redirect_uri": redirect_uri,
#         },
#         timeout=20,
#     )
#     resp.raise_for_status()
#     j = resp.json()
#     return j["access_token"], j.get("refresh_token")


# # Example one-time usage:
# print(get_auth_url(CLIENT_ID, REDIRECT_URI))
# access_token, refresh_token = exchange_code_for_tokens(AUTH_CODE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
# print("refresh_token:", refresh_token)


# =======================
# ACTIVE
# =======================

def refresh_access_token(refresh_token: str, client_id: str, client_secret: str) -> str:

    auth_b64 = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def get_recently_played_tracks(access_token: str, limit: int = 50):

    resp = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"limit": limit},
        timeout=20,
    )

    if resp.status_code == 204 or not resp.content:
        return []

    if not resp.ok:
        raise RuntimeError(f"Spotify error {resp.status_code}: {resp.text}")

    return resp.json().get("items", [])


# =======================
# MAIN
# =======================
if __name__ == "__main__":

    access_token = refresh_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
    items = get_recently_played_tracks(access_token, limit=50)

    for item in items:
        track = item.get("track") or {}
        song = track.get("name", "Unknown Song")
        artists = track.get("artists", [])
        artist_names = ", ".join(a.get("name", "Unknown Artist") for a in artists) or "Unknown Artist"

        print(f"{song} — {artist_names}")
