import time

import bs4
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

oceansURL = {
    'Atlantic Ocean': "https://www.wunderground.com/hurricane/archive/AL",
    'East Pacific': "https://www.wunderground.com/hurricane/archive/EP",
    'Western Pacific': "https://www.wunderground.com/hurricane/archive/WP",
    'Indian Ocean': "https://www.wunderground.com/hurricane/archive/IO",
    'Central Pacific': "https://www.wunderground.com/hurricane/archive/CP",
    'Southern Hemisphere': "https://www.wunderground.com/hurricane/archive/SH"
}


def getStormRecords(soup, year, ocean, years, oceans, dates, hours, windPower, airPressure,
                    stormType, stormNames, latCorr, longCorr):
    stormName = driver.find_element(By.CLASS_NAME, 'sub-header').text
    stormName = stormName.split(' ')[1]
    rows = soup.find('tbody').find_all('tr')
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
    print(storm.text)
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
    print(pd.DataFrame({'storm_name': stormNames, 'oceans': ocean, 'year': years, 'date': dates, 'time': hours,
                        'wind_power': windPower,
                        'air_pressure': airPressure, 'storm_type': stormType, 'lat': latCorr, 'long': longCorr}))


yearOfStorm = []
oceans = []
dates = []
hours = []
stormsName = []
stormType = []
latCorr = []
longCorr = []
windPower = []
airPressure = []
deaths = []
damagedUsd = []
website = 'https://www.wunderground.com/hurricane/archive/AL'
s = Service("C:/Program Files/chromeDriver/chromedriver.exe")
driver = webdriver.Chrome(service=s)
scrapDataFromCurrYear(2018, 'Atlantic Ocean', yearOfStorm, oceans, dates, hours, windPower, airPressure,
                      stormType, stormsName, latCorr, longCorr)

driver.quit()
