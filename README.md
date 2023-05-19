# Text2Spotify

Text2Spotify is a Python script that generates a Spotify playlist based on a text file. Each line in the text file represents a track name, and the script searches for these tracks on Spotify and adds them to a playlist.

## Prerequisites

To use Text2Spotify, you need to have the following:

- Python 3.x installed on your system.
- A Spotify developer account to obtain the necessary credentials.

## Installation

1. Clone or download the Text2Spotify project from the GitHub repository.

2. Install the required dependencies by running this command:

```
pip install spotipy
```


3. Obtain Spotify API credentials:
- Create a Spotify developer account and create a new application.
- Copy the Client ID and Client Secret and update the corresponding fields in the `config.py` file.

4. Provide the necessary information in the `config.py` file:
- `CLIENT_ID`: Your Spotify API client ID.
- `CLIENT_SECRET`: Your Spotify API client secret.
- `PLAYLIST_URL`: (Optional) URL of an existing Spotify playlist to add the tracks to. Leave it blank to create a new playlist.
- `TEXT_FILE`: (Optional) Path to the text file containing the track names. Leave it blank to use the default file named "music.txt" in the project directory.

## Usage

1. Open a terminal or command prompt and navigate to the project directory.

2. Run the `main.py` script:
```
python main.py
```

3. The script will authenticate with Spotify using your API credentials and create or retrieve the target playlist.

4. The script will read the song names from the file and add each song to the playlist.