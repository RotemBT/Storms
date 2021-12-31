# Import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By

def crawling_table():
    # url of the web
    # url = "https://www.wunderground.com/hurricane/archive/WP"

    # urls of 6 oceans
    all_url = ['https://www.wunderground.com/hurricane/archive/AL', "https://www.wunderground.com/hurricane/archive/EP",
               "https://www.wunderground.com/hurricane/archive/WP",
               "https://www.wunderground.com/hurricane/archive/IO", "https://www.wunderground.com/hurricane/archive/CP",
               "https://www.wunderground.com/hurricane/archive/SH"]

    # path of chrome_driver at specific computer
    s = Service('C:/Users/sapir/Documents/Storms/chromedriver.exe')
    years = []
    storms = []
    maxWinds = []
    minPressure = []
    storm_type = []
    storms_names = []
    hurricanes = []
    deaths = []
    damanged_usd = []
    for url in all_url:
        driver = webdriver.Chrome(service=s)
        driver.get(url)
        c = driver.page_source
        bs = BeautifulSoup(c, "html.parser")

        tdOfYear = bs.find_all('td', {'class': 'mat-cell cdk-cell cdk-column-year mat-column-year ng-star-inserted'})
        tdOfStorm = bs.find_all('td', {'class': 'mat-cell cdk-cell cdk-column-storms mat-column-storms ng-star-inserted'})
        tdOHurricanes = bs.find_all('td', {'class': 'mat-cell cdk-cell cdk-column-hurricanes mat-column-hurricanes ng-star-inserted'})
        tdOfDeaths = bs.find_all('td', {'class': 'mat-cell cdk-cell cdk-column-deaths mat-column-deaths ng-star-inserted'})
        tdOfDamanged_usd = bs.find_all('td', {'class': 'mat-cell cdk-cell cdk-column-damage mat-column-damage ng-star-inserted'})

        for td in tdOfYear:
            years.append(td.find('a').text)
            next_page = url + "/" + td.find('a').text

            # update path of next page
            driver.get(next_page)
            c = driver.page_source
            bs = BeautifulSoup(c, "html.parser")

            tdStormsNames = bs.find_all('td',{'class':'mat-cell cdk-cell cdk-column-summaryStormName mat-column-summaryStormName ng-star-inserted'})
            toOfMaxWinds = bs.find_all('td', {'class': 'mat-cell cdk-cell cdk-column-highestMaximumSustainedWind mat-column-highestMaximumSustainedWind ng-star-inserted'})
            tdOfMinPressure = bs.find_all('td',{'class':'mat-cell cdk-cell cdk-column-lowestMinimumPressure mat-column-lowestMinimumPressure ng-star-inserted'})
            tdOfMaxStrength = bs.find_all('td',{'class':'mat-cell cdk-cell cdk-column-maximumStormType mat-column-maximumStormType ng-star-inserted'})
            for i in tdStormsNames:
                storms_names.append(i.find('a').text)

            for i in toOfMaxWinds:
                try:
                    maxWinds.append(int(i.find('span').text))
                except:
                    maxWinds.append(0)
            print(maxWinds)
                
            for i in tdOfMinPressure:
                #print(i.find('span').text)
                try:
                    minPressure.append(i.find('span').text)
                except:
                    minPressure.append(0)
            print(minPressure)

            for i in tdOfMaxStrength:
                storm_type.append(i.text)

        for td in tdOfStorm:
            storms.append(td.find('span').text)
        for td in tdOHurricanes:
            hurricanes.append(td.find('span').text)
        for td in tdOfDeaths:
            deaths.append(td.find('span').text)
        for td in tdOfDamanged_usd:
            damanged_usd.append(td.find('span').text)

        driver.close()
    d = {'years': years, 'storms': storms, 'hurricanes': hurricanes, 'death': deaths, 'damanged_usd': damanged_usd}
    d2 = {'storms_names': storms_names, 'max_winds':maxWinds, 'max_strength':storm_type}
    df = pd.DataFrame(data=d)
    df2 = pd.DataFrame(data=d2)
    print(df)
    print(df2)
    df.to_csv('storms_df.csv')


if __name__ == '__main__':
    crawling_table()
