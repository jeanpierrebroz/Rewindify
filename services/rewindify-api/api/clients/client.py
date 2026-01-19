from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import urllib.parse
import requests
load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"
auth_code = os.getenv("SPOTIFY_AUTH_CODE")
refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

def get_token():

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    
    return token

def get_authorize_url(client_id, redirect_uri):
    scope = "user-read-recently-played"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
    }
    return "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)

def get_user_token(auth_code, client_id, client_secret, redirect_uri):
    auth_string = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_string.encode()).decode()

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
    }

    resp = requests.post(url, headers=headers, data=data)
    resp.raise_for_status()
    j = resp.json()
    return j["access_token"], j.get("refresh_token")



# print(get_authorize_url(client_id, REDIRECT_URI))


def refresh_access_token(refresh_token: str, client_id: str, client_secret: str) -> str:
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def get_recently_played_tracks(token: str, limit: int = 50):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers, params={"limit": limit})

    # Spotify can return 204 (no content) for some player endpoints.
    if resp.status_code == 204 or not resp.content:
        return []

    # If it's an error, show the actual message
    if not resp.ok:
        raise RuntimeError(f"Spotify error {resp.status_code}: {resp.text}")

    # Parse JSON safely
    return resp.json().get("items", [])

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

access_token = refresh_access_token(refresh_token, client_id, client_secret)
tracks = get_recently_played_tracks(access_token, limit=50)

for item in tracks:
    track = item["track"]
    song = track["name"]
    artist = track["artists"][0]["name"]

    print(f"{song}")




# access_token, refresh_token = get_user_token(
#     auth_code, client_id, client_secret, REDIRECT_URI
# )
# print("access:", access_token[:20], "...")
# print("refresh:", refresh_token[:20], "...")


# access_token, refresh_token = get_user_token(
#     auth_code,
#     client_id,
#     client_secret,
#     REDIRECT_URI,
# )
# print("got token")
# print(refresh_token)

# load_dotenv()
# client_id = os.getenv("SPOTIFY_CLIENT_ID")
# client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# def get_token():

#     auth_string = client_id + ":" + client_secret
#     auth_bytes = auth_string.encode("utf-8")
#     auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

#     url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": "Basic " + auth_base64,
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data = {"grant_type": "client_credentials"}
#     result = post(url, headers=headers, data=data)
#     json_result = json.loads(result.content)
#     token = json_result["access_token"]
    
#     return token

# def get_auth_header(token):
#     return {"Authorization": "Bearer " + token}

# def search_for_artist(token, artist_name):
#     url = "https://api.spotify.com/v1/search"
#     headers = get_auth_header(token)
#     query = f"?q={artist_name}&type=artist&limit=1"

#     query_url = url + query
#     result = get(query_url, headers=headers)
#     json_result = json.loads(result.content)["artists"]["items"]

#     if len(json_result) == 0:
#         print("No results")
#         return None

#     return json_result[0]

# token = get_token()
# search_artist = "blonk 183"
# res = search_for_artist(token, search_artist)
# print(f"Searching for: {search_artist}")
# print(f"Top Result: {res["name"]}")