import re
import bs4
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

LAST_YEAR = 2021
FIRST_YEAR = 1851
oceansURL = {
    'Atlantic Ocean': "https://www.wunderground.com/hurricane/archive/AL",
    'East Pacific': "https://www.wunderground.com/hurricane/archive/EP",
    'Western Pacific': "https://www.wunderground.com/hurricane/archive/WP",
    'Indian Ocean': "https://www.wunderground.com/hurricane/archive/IO",
    'Central Pacific': "https://www.wunderground.com/hurricane/archive/CP",
    'Southern Hemisphere': "https://www.wunderground.com/hurricane/archive/SH"
}


# Return bs4 instance
def urlToScrap(url):
    """
    get instance of soup to scarp from current url
    :param url: url to scrap
    :return: instance of soup
    """
    r = requests.get(url)
    return bs4.BeautifulSoup(r.content, 'html.parser')


# Crawling from wikipedia
def scrapFromWiki(yearCurr, soup, stormName, datesActive, stormCategory, maxMinWind, minPressure,
                  damageUSD, deaths, year):
    """
    this function scrap from wikipedia.
    link - https://en.wikipedia.org/wiki/Atlantic_hurricane_season
    :param yearCurr: current year of storm
    :param soup: get
    :param stormName:
    :param datesActive:
    :param stormCategory:
    :param maxMinWind:
    :param minPressure:
    :param damageUSD:
    :param deaths:
    :param year:
    :return:
    """
    ourTable = soup.find_all('table', class_='wikitable')
    trs = ourTable[-1].find_all("tr")
    for tr in trs[1:-2]:
        name = tr.find('th')
        stormName.append(name.text.strip())
        tData = tr.find_all("td")
        datesActive.append(tData[0].text.strip())
        stormCategory.append(tData[1].text.strip())
        maxMinWind.append(tData[2].text.strip())
        minPressure.append(tData[3].text.strip())
        damageUSD.append(tData[5].text.strip())
        deaths.append(tData[6].text.strip())
        year.append(str(yearCurr))


def scrapGeneralInformationOfOcean(oceansURL):
    years = []
    storms = []
    hurricanes = []
    deaths = []
    damagedUSD = []
    oceans = []
    for ocean, url in oceansURL.items():
        s = Service("C:/Program Files/chromeDriver/chromedriver.exe")
        driver = webdriver.Chrome(service=s)
        driver.get(url)
        c = driver.page_source
        soup = bs4.BeautifulSoup(c, "html.parser")
        tdOfYear = soup.find_all('td',
                                 class_='mat-cell cdk-cell cdk-column-year mat-column-year ng-star-inserted')
        tdOfStorm = soup.find_all('td',
                                  class_='mat-cell cdk-cell cdk-column-storms mat-column-storms ng-star-inserted')
        tdOHurricanes = soup.find_all('td',
                                      class_='mat-cell cdk-cell cdk-column-hurricanes mat-column-hurricanes'
                                             ' ng-star-inserted')
        tdOfDeaths = soup.find_all('td',
                                   class_='mat-cell cdk-cell cdk-column-deaths mat-column-deaths ng-star-inserted')
        tdOfDamagedUsd = soup.find_all('td',
                                       class_='mat-cell cdk-cell cdk-column-damage mat-column-damage ng-star-inserted')
        tdOfDamagedUsd = [damage.text for damage in tdOfDamagedUsd]
        tdOfDamagedUsd = [re.sub("[^0-9]", "", str(damage)) for damage in tdOfDamagedUsd]
        tdOfDeaths= [deaths.text for deaths in tdOfDeaths]
        tdOfDeaths =[re.sub("[^0-9]", "", str(deaths)) for deaths in tdOfDeaths]
        years.extend([year.text for year in tdOfYear])
        storms.extend([storm.text for storm in tdOfStorm])
        hurricanes.extend([hurricane.text for hurricane in tdOHurricanes])
        deaths.extend(tdOfDeaths)
        damagedUSD.extend(tdOfDamagedUsd)
        oceans.extend([ocean] * len(tdOfYear))
    return pd.DataFrame({'Years': years, 'Storms': storms, 'Hurricanes': hurricanes, 'Deaths': deaths,
                        'DamageUSD': damagedUSD, 'Oceans': oceans})

