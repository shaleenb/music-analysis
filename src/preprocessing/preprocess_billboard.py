"""Preprocess Billboard Data

This module performs preprocessing on the Billboard Hot 100 data extracted using the Billboard scraper.

Functions:
    clean_data(df_billboard) -> pandas.DataFrame
    clean_data(df_billboard) -> pandas.DataFrame
    clean_data(df_billboard) -> pandas.DataFrame
"""

import re
import unidecode
import pandas as pd


def clean_strings(df_billboard: pd.DataFrame) -> pd.DataFrame:
    """Cleans the song title and artist name fields.
    Performs the following operations:
        Replace '&' with 'and'
        Replace '-' with ' '
        Remove all special characters
        Remove all accents

    Args:
        df_billboard (pd.DataFrame): DataFrame with Billboard data

    Returns:
        df_billboard: Cleaned up DataFrame
    """

    def clean(string: str) -> str:
        string = string.replace("&", "and")
        string = string.replace("-", " ")
        string = re.sub(r"[^\w\s.,]", "", string)
        string = unidecode.unidecode(string)
        string = string.strip()
        string = string.lower()
        return string

    df_billboard[["song", "artist"]] = df_billboard[["song", "artist"]].applymap(clean)

    return df_billboard


def separate_artists(df_billboard: pd.DataFrame) -> pd.DataFrame:
    """Splits the artist field into main and featuring artists, and drops the original artist column.

    Args:
        df_billboard (pd.DataFrame): DataFrame with Billboard data

    Returns:
        df_billboard (pd.DataFrame): DataFrame with artist column split into main_artist, other_artist and featuring_artist columns.
    """

    df_billboard[["main_artist", "featuring_artist"]] = df_billboard[
        "artist"
    ].str.split(" featuring ", expand=True)
    df_billboard["main_artist"] = df_billboard["main_artist"].str.replace(" and", ",")
    df_billboard[["main_artist", "other_artist"]] = df_billboard[
        "main_artist"
    ].str.split(",", n=1, expand=True)
    df_billboard = df_billboard.drop("artist", axis=1)
    return df_billboard


def resolve_ties(df_billboard: pd.DataFrame) -> pd.DataFrame:
    """Some rows in the data have 'Tie' in the rank column. This function replaces 'Tie' with the previous row's rank.

    Args:
        df_billboard (pd.DataFrame): DataFrame with Billboard data

    Returns:
        df_billboard (pd.DataFrame): DataFrame with ties resolved and rank column converted to int type.
    """

    df_billboard["rank"] = df_billboard["rank"].replace("Tie")
    df_billboard["rank"] = df_billboard["rank"].astype(int)

    return df_billboard


def main():
    """Preprocess Billboard Data
    """

    df_billboard = pd.read_csv("./../data/raw/billboard.csv")
    df_billboard = clean_strings(df_billboard)
    df_billboard = separate_artists(df_billboard)
    df_billboard = resolve_ties(df_billboard)

    df_billboard.to_csv("../../data/processed/billboard.csv", index=False)


if __name__ == "__main__":
    main()
