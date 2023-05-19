import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, PLAYLIST_URL, TEXT_FILE


def create_spotify_playlist():
    if not CLIENT_ID:
        raise ValueError("CLIENT_ID is missing in config.py")

    if not CLIENT_SECRET:
        raise ValueError("CLIENT_SECRET is missing in config.py")

    scope = "playlist-read-collaborative " \
            "playlist-modify-public " \
            "playlist-modify-private " \
            "playlist-read-private "

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri="http://localhost:8080/callback/",
                                                   scope=scope))

    return sp


def create_default_playlist(sp):
    if len(PLAYLIST_URL) == 0:
        playlist_name = "Text2Spotify Playlist"
        user_id = sp.me()["id"]
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, description="This playlist was generated using Text2Spotify")
        playlist_url = playlist["external_urls"]["spotify"]
        print(f"Created a new playlist: {playlist_url}")
        return playlist_url
    else:
        return PLAYLIST_URL


def add_tracks_to_playlist(sp, playlist_url, tracks):
    if len(tracks) > 0:
        sp.playlist_add_items(playlist_url, tracks)
        print("Added tracks to the playlist")
        return True
    else:
        print("No tracks to add to the playlist")
        return False


def search_track(sp, track_name):
    song = sp.search(track_name)
    try:
        song_id = song["tracks"]["items"][0]["uri"]
        song_name = song["tracks"]["items"][0]["name"]
    except IndexError:
        print(f"{track_name} is not found on Spotify")
        return None, None
    return song_id, song_name


def process_text_file(sp, playlist_url, text_file):
    track_ids = []
    playlist_data = sp.playlist(playlist_url)
    amount = min(100, playlist_data["tracks"]["total"])

    try:
        with open(text_file, encoding="utf8") as f:
            for line in f.readlines():
                track_name = line.strip()
                found = False
                song_id, song_name = search_track(sp, track_name)
                if song_id is None:
                    continue

                if len(track_ids) == 99:
                    add_tracks_to_playlist(sp, playlist_url, track_ids)
                    track_ids.clear()
                    track_ids.append(song_id)
                    continue
                else:
                    #  Prevent duplicate songs
                    #  Uses URI instead of name because every song has a unique URI
                    for j in range(amount):
                        if song_id == playlist_data["tracks"]["items"][j]["track"]["uri"]:
                            print(f'{playlist_data["tracks"]["items"][j]["track"]["name"]} is already in the playlist')
                            found = True
                            break

                if found:
                    continue

                if song_id in track_ids:
                    continue
                
                print(f'Adding "{song_name}" to the playlist')
                track_ids.append(song_id)

            add_tracks_to_playlist(sp, playlist_url, track_ids)
        
    except FileNotFoundError:
        print(f"Text file '{text_file}' not found")


def main():
    sp = create_spotify_playlist()
    playlist_url = create_default_playlist(sp)
    text_file = TEXT_FILE
    if not text_file:
        text_file = "music.txt"
    process_text_file(sp, playlist_url, text_file)


if __name__ == "__main__":
    main()
