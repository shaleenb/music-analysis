"""Preprocess Spotify Data.

Functions:
    drop_and_rearrange_columns(dataframe, columns_to_keep) -> pd.DataFrame

"""

from __future__ import annotations
import pandas as pd


def drop_and_rearrange_columns(
    dataframe: pd.DataFrame, columns_to_keep: list[str]
) -> pd.DataFrame:
    """Drops and rearranges columns of a Pandas DataFrame.

    Args:
        dataframe (pd.DataFrame): Dataframe to operate on.
        columns_to_keep (list[str]): List of columns to keep in the order wanted.

    Returns:
        (pd.DataFrame): DataFrame with required columns
    """

    return dataframe[columns_to_keep]


def join_with_billboard(df_spotify: pd.DataFrame, df_billboard: pd.DataFrame) -> pd.DataFrame:
    """Perform inner join with Billboard data

    Args:
        df_spotify (pd.DataFrame): DataFrame with Spotify data
        df_billboard (pd.DataFrame): DataFrame with Billboard data

    Returns:
        pd.DataFrame: Merged DataFrame
    """

    df_merged = pd.merge(left=df_spotify, right=df_billboard, left_on='billboard_df_index', right_index=True)

    return df_merged

def main():
    """Preprocess Spotify Data
    """

    df_spotify = pd.read_csv("./../data/raw/spotify.csv")

    # Convert duration to minutes
    df_spotify["duration_minutes"] = df_spotify["duration_ms"] / 60000

    columns_to_keep = [
        "spotify_song",
        "spotify_artist",
        "duration_minutes",
        "popularity",
        "explicit",
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "key",
        "liveness",
        "loudness",
        "mode",
        "speechiness",
        "tempo",
        "time_signature",
        "valence",
        "billboard_df_index",
    ]

    df_spotify = drop_and_rearrange_columns(df_spotify, columns_to_keep)

    df_spotify.to_csv("../../data/processed/spotify.csv", index=False)

    df_billboard = pd.read_csv("../../data/processed/billboard.csv")

    df_merged = join_with_billboard(df_spotify, df_billboard)
    df_merged.to_csv("./../data/processed/spotify-billboard.csv", index=False)


if __name__ == "__main__":
    main()
