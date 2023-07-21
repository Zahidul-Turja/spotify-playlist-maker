import pprint
import os

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECTET")
REDIRECT_URL = "http://example.com"
SCOPE = "playlist-modify-private"
PLAYLIST_DATE = "2020-08-12"
PLAYLIST_NAME = f"{PLAYLIST_DATE} Billboard 100"


# sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
# result = sp.search(song_name)

# parsing HTML
# input("Which year do you want to travel to? (YYYY-MM-DD)")
user_date = PLAYLIST_DATE
page = requests.get(f"https://www.billboard.com/charts/hot-100/{user_date}/")
soup = BeautifulSoup(page.text, 'html.parser')
temp_titles = soup.select("li.o-chart-results-list__item "
                          "h3#title-of-a-story.c-title")
temp_singers = soup.select("li.o-chart-results-list__item "
                           "span.c-label.a-no-trucate")

# Filtering titles
titles = {}
titles_list = []
for t, item in enumerate(temp_titles):
    # titles[t+1] = item.getText().strip()
    titles_list.append(item.getText().strip())

# for item in titles_list:
#     print(item)

# USER AUTH START
spotify = SpotifyOAuth(client_id=CLIENT_ID,
                       client_secret=CLIENT_SECRET,
                       redirect_uri=REDIRECT_URL,
                       scope=SCOPE,
                       show_dialog=True,
                       cache_path="token.txt"
                       )
sp = spotipy.Spotify(auth_manager=spotify)
# USER AUTHO END

# URIs of 100 SONGS start
items = []
for item in titles_list:
    items.append(sp.search(item))

user_id = sp.current_user()["id"]
tracks = []
for result in items:
    tracks.append(result["tracks"]["items"][0]["uri"])
# URI of 100 SONGS end

# CREATING PLAYLIST
created_playlist = sp.user_playlist_create(user=user_id,
                                           name=PLAYLIST_NAME,
                                           public=False,
                                           description="Billboard 100 Songs of the day")

playlist_id = created_playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id,
                      items=tracks)


# CREATING PLAYLIST END


# UNN
# for i, title in titles.items():
#     print(f"{i}. {title}")
#
# Filtering Singers
# singers = {}
# for t, item in enumerate(temp_singers):
#     singers[t+1] = item.getText().strip()
#
# for i, singer in singers.items():
#     print(f"{i}. {singer}")
