# Import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd


def crawling_table():
    # url of the web
    url = "https://www.wunderground.com/hurricane/archive/WP"

    """
    # urls of 6 oceans
    all_url =['https://www.wunderground.com/hurricane/archive/AL',"https://www.wunderground.com/hurricane/archive/EP","https://www.wunderground.com/hurricane/archive/WP",
          "https://www.wunderground.com/hurricane/archive/IO","https://www.wunderground.com/hurricane/archive/CP","https://www.wunderground.com/hurricane/archive/SH"]
    """

    # path of chrome_driver at specific computer
    s = Service('C:/Users/sapir/Documents/Storms/chromedriver.exe')

    # web_driver object
    driver = webdriver.Chrome(service=s)
    driver.get(url)

    c = driver.page_source
    bs = BeautifulSoup(c, "html.parser")

    years = []
    storms = []
    hurricanes = []
    deaths = []
    damanged_usd = []
    tdOfYear = bs.find_all('td', {'class': 'mat-cell cdk-cell cdk-column-year mat-column-year ng-star-inserted'})
    tdOfStorm = bs.find_all('td', {'class': 'mat-cell cdk-cell cdk-column-storms mat-column-storms ng-star-inserted'})
    tdOHurricanes = bs.find_all('td', {'class': 'mat-cell cdk-cell cdk-column-hurricanes mat-column-hurricanes ng-star-inserted'})
    tdOfdeaths = bs.find_all('td', {'class': 'mat-cell cdk-cell cdk-column-deaths mat-column-deaths ng-star-inserted'})
    tdOfdamanged_usd = bs.find_all('td', {'class': 'mat-cell cdk-cell cdk-column-damage mat-column-damage ng-star-inserted'})

    for td in tdOfYear:
        years.append(td.find('a').text)
    for td in tdOfStorm:
        storms.append(td.find('span').text)
    for td in tdOHurricanes:
        hurricanes.append(td.find('span').text)
    for td in tdOfdeaths:
        deaths.append(td.find('span').text)
    for td in tdOfdamanged_usd:
        damanged_usd.append(td.find('span').text)
    d={'years':years,'storms':storms,'hurricanes':hurricanes,'death':deaths,'damanged_usd':damanged_usd}
    df = pd.DataFrame(data=d)
    print(df)
    driver.close()


if __name__ == '__main__':
    crawling_table()