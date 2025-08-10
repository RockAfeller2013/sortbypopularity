MP3 Popularity Sorter Setup Guide
This script sorts .mp3 files in a folder based on their popularity and renames them in ranked order.
It supports Spotify API for current popularity and Last.fm API for lifetime play counts.

1. Prerequisites
Python 3.7+

pip package manager

Internet connection

2. Install Dependencies
bash
Copy
Edit
pip install spotipy requests
3. API Setup
Option A – Spotify API (Current Popularity)
Go to Spotify Developer Dashboard and create an app.

Copy your Client ID and Client Secret.

Set them as environment variables:

Linux/macOS:

bash
Copy
Edit
export SPOTIPY_CLIENT_ID="your_spotify_client_id"
export SPOTIPY_CLIENT_SECRET="your_spotify_client_secret"
Windows (PowerShell):

powershell
Copy
Edit
setx SPOTIPY_CLIENT_ID "your_spotify_client_id"
setx SPOTIPY_CLIENT_SECRET "your_spotify_client_secret"
Option B – Last.fm API (Lifetime Popularity)
Create a Last.fm API account: https://www.last.fm/api/account/create

Copy your API Key.

Set it as an environment variable:

Linux/macOS:

bash
Copy
Edit
export LASTFM_API_KEY="your_lastfm_api_key"
Windows (PowerShell):

powershell
Copy
Edit
setx LASTFM_API_KEY "your_lastfm_api_key"
4. Usage
bash
Copy
Edit
python sort_mp3_by_popularity.py /path/to/mp3/folder
The script will:

Fetch popularity for each .mp3 file.

Sort from most popular to least.

Rename each file with a zero-padded rank (00001_song.mp3).

5. Notes
Spotify returns a popularity score (0–100) based on recent trends.

Last.fm returns a total play count (lifetime).

If a track is not found, it will be placed at the end in alphabetical order.

Duplicate filenames are handled automatically to prevent overwriting.
