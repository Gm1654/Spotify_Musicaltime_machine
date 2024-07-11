import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime as dt

# Input for the date
year = input("Enter the year (YYYY): ")
month = input("Enter the month (MM): ")
day = input("Enter the day (DD): ")
date = f"{year}-{month}-{day}"
month_name = dt.strptime(f"{month}", "%m").strftime("%B")

# Fetch Billboard Hot 100 for the given date
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
billboard = response.text
soup = BeautifulSoup(billboard, "html.parser")
all_titles = soup.select("li span.chart-element__information__song")
titles = [title.getText().strip() for title in all_titles[:100]]

# Initialize Spotify client with correct credentials
sp = spotipy.Spotify(  
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="128f2d05ce364c30a9127a07fa703e44",
        client_secret="4613106ec0ec40699047ff7fb3341585",
        cache_path="token.txt"
    )
)


# Create playlist and add tracks
playlist_name = f"Top 100 songs of {month_name} {day}, {year}"
user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
playlist_id = playlist['id']

# Search for each song and add to the playlist
for title in titles:
    results = sp.search(q=f"track:{title}", type="track")
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.playlist_add_items(playlist_id, [track_uri])
    else:
        print(f"Track '{title}' not found on Spotify.")

print(f"Playlist '{playlist_name}' created successfully.")

