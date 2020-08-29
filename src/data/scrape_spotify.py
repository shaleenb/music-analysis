"""This script uses the Spotify API to fetch additional data for songs.

Functions:
    query_spotify(songs_df, verbose) -> pd.DataFrame, pd.DataFrame
"""

from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
import spotipy
import spotipy.util
from tqdm import tqdm


def query_spotify(songs_df: pd.DataFrame, verbose=0) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Queries the spotify API by using the artist name and the song title.
    Primarily fetches song popularity and content-based information.
    Find more at https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

    Args:
        songs_df (pd.DataFrame): DataFrame containing songs for which Spotify must be queried. Must contain
                                 a column 'song' with the title of the song and a column 'artist' with the
                                 name of the artist
        verbose (int, optional): Logging verbosity. Three levels.
                                 0 - No logging.
                                 1 - Failure messages only.
                                 2 - Failure and success messages.
                                 Defaults to 0.

    Returns:
        df_audio_features (pd.DataFrame): DataFrame with audio features
        df_failed (pd.DataFrame): DataFrame with year, title and artist of failed queries.
    """

    # Create client
    spotify = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())

    failed = []
    track_data = []

    # Fetch Track URIs, popularity and explicitness.
    # Track URI is needed to query for audio features
    for index, row in tqdm(songs_df.iterrows()):
        title = row['song']
        artist = row['main_artist']
        year = row['year']
        try:
            results = spotify.search(q='track:' + title + ' artist:' + artist, type='track',
                                     limit=1)
            result = results['tracks']['items'][0]

            track_data.append({
                'spotify_uri': result['uri'],
                'spotify_song': result['name'],
                'spotify_artist': result['artists'][0]['name'],
                'popularity': result['popularity'],
                'explicit': result['explicit'],
                'billboard_df_index': index  # For joining in the future
            })

            if verbose > 1:
                print('Successfully queried song {}: {} by {}'.format(index, title, artist))

        except:
            if verbose > 0:
                print('Search failed for song {}: {} by {}'.format(index, title, artist))
            failed.append([title, artist, year])

    if verbose > 0:
        print('Unable to query {} songs'.format(len(failed)))

    df_failed = pd.DataFrame(failed, columns=['song', 'artist', 'year'])

    df_audio_features = pd.DataFrame()

    # Query in chunks of 100 to reduce network overhead
    for index in tqdm(range(0, len(track_data), 100)):
        uri_list = [track['spotify_uri'] for track in track_data[index: index + 100]]
        audio_features_list = spotify.audio_features(uri_list)

        for idx, audio_features in enumerate(audio_features_list):
            audio_features.pop('track_href')
            audio_features.pop('analysis_url')
            df_audio_features = df_audio_features.append({**track_data[index + idx], **audio_features},
                                                         ignore_index=True)

    return df_audio_features, df_failed


def plot_failed(df_failed: pd.DataFrame):
    """Creates a bar plot with number of failed queries in each year. Saves it as failed_spotify_queries.png.

    Args:
        df_failed (pd.DataFrame): DataFrame with songs that resulted in failed searches.
    """
    ax = (df_failed.year
          .value_counts()
          .sort_index()
          .plot.bar(figsize=(16,5), alpha=0.75))

    ax.yaxis.grid(True)
    ax.set(xlabel='year', ylabel='# failed queries')

    plt.savefig('../../reports/figures/failed_spotify_queries.png')


def main():
    """Fetch additional data for songs using the Spotify API.
    """
    songs_df = pd.read_csv('billboard_preprocessed.csv')
    df_audio_features, df_failed = query_spotify(songs_df, verbose=1)
    if not df_failed.empty:
        plot_failed(df_failed)
    df_audio_features.to_csv('../../data/raw/spotify.csv', index=False)


if __name__ == "__main__":
    main()
