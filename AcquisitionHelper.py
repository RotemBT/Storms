import re
import requests
import time
import numpy as np
import bs4
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

LAST_YEAR = 2021
FIRST_YEAR = 1950
oceansURL = {
    'Atlantic Ocean': "https://www.wunderground.com/hurricane/archive/AL",
    'East Pacific': "https://www.wunderground.com/hurricane/archive/EP",
    'Western Pacific': "https://www.wunderground.com/hurricane/archive/WP",
    'Indian Ocean': "https://www.wunderground.com/hurricane/archive/IO",
    'Central Pacific': "https://www.wunderground.com/hurricane/archive/CP",
    'Southern Hemisphere': "https://www.wunderground.com/hurricane/archive/SH"
}

SAPIR_LOCATION = 'C:/Users/sapir/Documents/Storms/chromedriver.exe'
ROTEM_LOCATION = "C:/Program Files/chromeDriver/chromedriver.exe"
website = 'https://www.wunderground.com/hurricane/archive/AL'
s = Service(ROTEM_LOCATION)
driver = webdriver.Chrome(service=s)


def getDataFrame(stormsName, yearOfStorm, oceans, dates, hours, windPower, airPressure, stormType, latCorr, longCorr):
    return pd.DataFrame(
        pd.DataFrame({'storm_name': stormsName, 'year': yearOfStorm, 'oceans': oceans, 'date': dates, 'time': hours,
                      'wind_power': windPower,
                      'air_pressure': airPressure, 'storm_type': stormType, 'lat': latCorr, 'long': longCorr}))


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


# Crawling general info from Wunderground
def scrapGeneralInformationOfOcean(oceansURL):
    years = []
    storms = []
    hurricanes = []
    deaths = []
    damagedUSD = []
    oceans = []
    for ocean, url in oceansURL.items():
        s = Service('C:/Users/sapir/Documents/Storms/chromedriver.exe')
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
        tdOfDeaths = [deaths.text for deaths in tdOfDeaths]
        tdOfDeaths = [re.sub("[^0-9]", "", str(deaths)) for deaths in tdOfDeaths]
        years.extend([year.text for year in tdOfYear])
        storms.extend([storm.text for storm in tdOfStorm])
        hurricanes.extend([hurricane.text for hurricane in tdOHurricanes])
        deaths.extend(tdOfDeaths)
        damagedUSD.extend(tdOfDamagedUsd)
        oceans.extend([ocean] * len(tdOfYear))
    return pd.DataFrame({'Years': years, 'Storms': storms, 'Hurricanes': hurricanes, 'Deaths': deaths,
                         'DamageUSD': damagedUSD, 'Oceans': oceans})


def getStormRecords(soup, year, ocean, years, oceans, dates, hours, windPower, airPressure,
                    stormType, stormNames, latCorr, longCorr):
    # Sleep for wait for the dynamic page will be loaded.
    time.sleep(2)
    stormName = driver.find_element(By.CLASS_NAME, 'sub-header').text
    stormName = stormName.split(' ')[1]
    stormName = 'NOT_NAMED' if stormName == 'NOT' else stormName
    try:
        rows = soup.find('tbody').find_all('tr')
    except:
        rows = []
    for row in rows:
        columns = row.find_all('td')
        years.append(year)
        oceans.append(ocean)
        stormNames.append(stormName)
        dates.append(columns[0].text)
        hours.append(columns[1].text)
        latCorr.append(columns[2].text)
        longCorr.append(columns[3].text)
        windPower.append(columns[4].text)
        airPressure.append(columns[5].text)
        stormType.append(columns[6].text)


def scrapDataFromCurrYear(year, ocean, years, oceans, dates, hours, windPower, airPressure,
                          stormType, stormNames, latCorr, longCorr):
    url = 'https://www.wunderground.com/hurricane/archive/AL/' + str(year)
    driver.get(url)
    time.sleep(5)
    storm = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/div/div/div[2]/div/div[3]'
                                          '/lib-storms-list/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/a')
    if storm.text != 'NOT_NAMED':
        storm.click()
        while True:
            driver.get(driver.current_url)
            c = driver.page_source
            soup = bs4.BeautifulSoup(c, "html.parser")
            getStormRecords(soup, year, ocean, years, oceans, dates, hours, windPower, airPressure,
                            stormType, stormNames, latCorr, longCorr)
            nextStorm = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/div/div/div[2]/div/div['
                                                      '2]/lib-storm/div/div/div[1]/ul/li[3]/a')

            if nextStorm.text != 'All Storms »':
                nextStorm.click()
            else:
                break
    else:
        driver.get(driver.current_url)
        c = driver.page_source
        soup = bs4.BeautifulSoup(c, "html.parser")
        try:
            rows = soup.find('tbody').find_all('tr')
        except:
            rows = []
        for row in rows:
            columns = row.find_all('td')
            startDate = str(columns[1].text).split(' - ')[1] + '/' + str(year)
            years.append(year)
            oceans.append(ocean)
            stormNames.append(columns[0].text)
            dates.append(startDate)
            hours.append('12:00:00 PM')
            latCorr.append(np.nan)
            longCorr.append(np.nan)
            windPower.append(columns[2].text)
            airPressure.append(columns[3].text)
            stormType.append(columns[4].text)


# Handling with missing data
"""
def emptyLon(lonCorr):
    sum1 = sum(lonCorr)
    return float(sum1 / len(lonCorr))
def emptyLat(latCorr):
    sum2 = sum(latCorr)
    return float(sum2 / len(latCorr))
def emptyMinPressure(airPressure):
    return min(airPressure)
"""


def fillMissingData(df):
    mean = df['airPressure'].mean()
    df['airPressure'].fillna(mean)

    mean = df['lonCorr'].mean()
    df['lonCorr'].fillna(mean)

    mean = df['latCorr'].mean()
    df['latCorr'].fillna(mean)
