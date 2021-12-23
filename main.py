# Import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup


def crawling_table():
    # url of the web
    url = "https://www.wunderground.com/hurricane/archive/WP"

    # path of chrome_driver at specific computer
    s = Service('C:/Users/sapir/Documents/Storms/chromedriver.exe')

    # web_driver object
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    c = driver.page_source
    bs = BeautifulSoup(c, "html.parser")
    table = bs.find_all('div', {'class': "storms-wrapper mat-elevation-z8 ng-star-inserted"})

    years = []
    storms = []
    hurricanes = []
    deaths = []
    damanged_usd = []

    # Find elements in table
    table_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//table[@class = 'mat-table cdk-table mat-sort']")))
    for table_element in table_elements:
        for row in table_element.find_elements(By.XPATH,".//tr"):
            print(row.text)
    """
    for t in table:
        print(driver.find_elements(By.CLASS_NAME,"storms-wrapper mat-elevation-z8 ng-star-inserted"))
       # x=t.find_all("tr").find_all("td").text
       # years.append(x)
    years
    """

    driver.close()


if __name__ == '__main__':
    crawling_table()