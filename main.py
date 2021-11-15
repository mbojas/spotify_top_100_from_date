from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

#dokumentacja spotipy: https://spotipy.readthedocs.io/en/2.13.0/#ids-uris-and-urls
#dokumentacja pprint: https://docs.python.org/3/library/pprint.html

SPOTIPY_CLIENT_ID = "INSERT YOUR CLIENT ID HERE"
SPOTIPY_CLIENT_SECRET = "INSERT YOUR SPOTIFY SECRET STRING HERE"

data = input("Write a date, that you want to travel to (YYYY-MM-DD):")
year = data.split("-")[0]
URL = "https://www.billboard.com/charts/hot-100/"+data


# SCRAPPER Z BILLBOARD.COM ----------------------------------------------------------------------------------------
response = requests.get(URL)
page = response.text
soup = BeautifulSoup(page, "html.parser")
utwory_spans = soup.find_all("span", class_="chart-element__information__song")
utwory_names = [utwor.getText() for utwor in utwory_spans]

# spotify authentication --------------------------------------------------------------------------------------------
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt")
)

user_id = sp.current_user()["id"]
utwory_uris = []

for song in utwory_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        utwory_uris.append(uri)
    except IndexError:
        print(f"{song} nie istnieje w spotify")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{data} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=utwory_uris)



