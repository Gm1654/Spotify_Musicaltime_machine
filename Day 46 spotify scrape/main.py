import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime as dt

year=input("what year do you would like to listen the song? ")
month=input("what month do you would like to listen the song? ")
day=input("what day do you would like to listen the song? ")
date=f"{year}-{month}-{day}"
month_name=dt.strptime(f"{month}","%m").strftime("%B")





response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
billboard = response.text
soup = BeautifulSoup(billboard, "html.parser")
all_titles = soup.select(selector="li h3", class_="c-title")
titles = [title.getText().strip() for title in all_titles[:100]]
print(titles)

sp = spotipy.Spotify(  
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="128f2d05ce364c30a9127a07fa703e44",
        client_secret="4613106ec0ec40699047ff7fb3341585",
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# print(user_id)


uri = []
for title in titles:
    result = sp.search(q=title, type='track')
    if result['tracks']['items']:
        uri.append(result['tracks']['items'][0]['uri'])

playlist_ID = sp.user_playlist_create(user=user_id, name=f"Top 100 songs of {year} {month_name} {day}", public=False)["id"]
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_ID, tracks=uri)


