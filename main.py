import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

date_entered = input("What date would you like to travel back in time to? Enter the dates in the format YYYY-MM-DD\n")

CLIENT_ID = os.environ["ENVIRON_ID"]
CLIENT_SECRET = os.environ["ENVIRON_SECRET"]
URL = f"https://www.billboard.com/charts/hot-100/{date_entered}/"
REDIRECT_URL = "http://example.com"

response = requests.get(URL)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

titles = soup.select("li ul li h3")
list_of_titles = [title.getText().strip() for title in titles]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope="playlist-modify-private"))

user_id = sp.current_user()["id"]

song_uris = [sp.search(song)["tracks"]["items"][0]["uri"] for song in list_of_titles]

playlist_id = sp.user_playlist_create(user=user_id,
                                      name="Time Travel Playlist",
                                      public=False)

sp.playlist_add_items(playlist_id=playlist_id["id"], items=song_uris)