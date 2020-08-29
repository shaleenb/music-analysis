"""Scrape Billboard Charts

This script scrapes Wikipedia to get a dataframe of the Billboard year-end Hot 100 songs.

Functions:
    prepare_driver() -> selenium.webdriver.Chrome
    scrape_for_year(driver, year) -> pandas.DataFrame
    scrape_for_range(driver, start_year, end_year) -> pandas.DataFrame
"""

from tqdm import tqdm
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


url_template = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year}"


def prepare_driver() -> Chrome:
    """Creates a ChromeDriver object. It has been configured to not load images.

    Returns:
        driver (selenium.webdriver.Chrome): The ChromeDriver object.
    """

    chrome_options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = Chrome(options=chrome_options)
    return driver


def scrape_for_year(driver: Chrome, year: int) -> pd.DataFrame:
    """Scrapes Wikipedia for Year end Billboard Hot 100 songs for the given year

    Args:
        driver (selenium.webdriver.Chrome): Selenium ChromeDriver object
        year (int): Year for which data should be scraped

    Returns:
        df_billboard (pd.DataFrame): Contains the rank, title and artist name for each song
    """

    url = url_template.format(year=year)
    driver.get(url)

    # Wait for the page to load
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "wikitable")))
    except TimeoutException:
        print("Skipping year {}".format(year))
        return pd.DataFrame()

    # Get table element
    table_element = driver.find_element_by_class_name("wikitable")

    # Get all rows inside the table
    table_rows = table_element.find_elements_by_tag_name("tr")[1:]

    data = []

    for row in table_rows:
        # Get all children of the row element
        rank, song, artist = map(lambda x: x.text, row.find_elements_by_xpath("*"))
        data.append({"rank": rank, "song": song.strip('"'), "artist": artist})

    df_hot100 = pd.DataFrame(data=data)
    return df_hot100


def scrape_for_range(driver: Chrome, start_year: int, end_year: int) -> pd.DataFrame:
    """Scrapes Wikipedia for Year end Billboard Hot 100 songs for the years in range [start_year, end_year).
    Uses scrape_for_year.

    Args:
        driver (selenium.webdriver.Chrome): Selenium ChromeDriver object
        start_year (int): Starting year (inclusive)
        end_year (int): Ending year (exclusive)

    Returns:
        df_billboard (pd.DataFrame): Contains the year, rank, title and artist name for each song
    """
    df_billboard = pd.DataFrame()

    for year in tqdm(range(start_year, end_year)):
        df_year = scrape_for_year(driver, year)
        df_billboard = df_billboard.append(df_year)

    return df_billboard


def main():
    """This script scrapes Wikipedia to get a dataframe of the Billboard year-end Hot 100 songs
    """

    driver = prepare_driver()
    df_billboard = scrape_for_range(driver, start_year=1960, end_year=2020)
    df_billboard.to_csv("../../data/raw/billboard.csv", index=False)


if __name__ == "__main__":
    main()
