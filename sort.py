import os
import sys
import requests

LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")

if not LASTFM_API_KEY:
    print("Error: Please set your Last.fm API key in the environment variable LASTFM_API_KEY")
    sys.exit(1)

def get_lastfm_playcount(track_name):
    """
    Fetch the playcount for a given track using Last.fm API.
    We try without artist info since filenames often don't have it.
    """
    try:
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "track.search",
            "track": track_name,
            "api_key": LASTFM_API_KEY,
            "format": "json",
            "limit": 1
        }
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()

        results = data.get("results", {}).get("trackmatches", {}).get("track", [])
        if isinstance(results, dict):
            results = [results]  # Handle single result case

        if results:
            playcount = results[0].get("playcount")
            if playcount is not None:
                return int(playcount)
    except Exception as e:
        print(f"Error fetching playcount for '{track_name}': {e}")
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python sort_mp3_by_lastfm.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        sys.exit(1)

    mp3_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mp3')]
    if not mp3_files:
        print("No .mp3 files found in the specified folder.")
        sys.exit(0)

    file_data = []
    print("Fetching playcounts from Last.fm...")
    for f in mp3_files:
        track_name = os.path.splitext(f)[0]
        playcount = get_lastfm_playcount(track_name)
        file_data.append((f, playcount))
        print(f" - {f}: {'Not found' if playcount is None else playcount}")

    found_tracks = [fd for fd in file_data if fd[1] is not None]
    not_found_tracks = [fd for fd in file_data if fd[1] is None]

    found_tracks.sort(key=lambda x: x[1], reverse=True)
    not_found_tracks.sort(key=lambda x: x[0].lower())

    sorted_files = found_tracks + not_found_tracks

    print("\nRenaming files...")
    for idx, (filename, _) in enumerate(sorted_files, start=1):
        new_name = f"{idx:05d}_{filename}"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        counter = 1
        while os.path.exists(new_path):
            base, ext = os.path.splitext(new_name)
            new_name = f"{base}_{counter}{ext}"
            new_path = os.path.join(folder_path, new_name)
            counter += 1

        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")

    print("\nDone.")

if __name__ == "__main__":
    main()
