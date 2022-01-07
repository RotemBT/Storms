from selenium import webdriver
oceansURL = {
    'Atlantic Ocean': "https://www.wunderground.com/hurricane/archive/AL",
    'East Pacific': "https://www.wunderground.com/hurricane/archive/EP",
    'Western Pacific': "https://www.wunderground.com/hurricane/archive/WP",
    'Indian Ocean': "https://www.wunderground.com/hurricane/archive/IO",
    'Central Pacific': "https://www.wunderground.com/hurricane/archive/CP",
    'Southern Hemisphere': "https://www.wunderground.com/hurricane/archive/SH"
}
def scrapDataFromCurrYear(year):
    url = 'https://www.wunderground.com/hurricane/archive/AL/' + str(year)
    driver.get(url)
    storm = driver.find_element_by_tag_name('td').find_element_by_tag_name('a')
    print(driver.current_url)
    print(storm.text)
    storm.click()
    driver.get(driver.current_url)
    element = driver.find_element_by_tag_name('td')
    print(element.text)


website = 'https://www.wunderground.com/hurricane/archive/AL'
path = "C:/Program Files/chromeDriver/chromedriver.exe"
driver = webdriver.Chrome(path)
scrapDataFromCurrYear(2021)

driver.quit()
