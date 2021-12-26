import bs4
import requests
import pandas as pd
import time

# Return bs4 instance
def urlToScrap(url):
    r = requests.get(url)
    return bs4.BeautifulSoup(r.content, 'html.parser')


# Crawling from wikipedia
def scrapFromWiki(yearCurr, soup, stormName, datesActive, stormCategory, maxMinWind, minPressure,
                  damageUSD, deaths, year):
    outTable = soup.find_all('table', class_='wikitable')
    trs = outTable[-1].find_all("tr")
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

start =time.time()
stormName = []
datesActive = []
stormCategory = []
maxMinWind = []
minPressure = []
areasAffected = []
damageUSD = []
deaths = []
year = []
for i in range(1940, 2022):
    try:
        print(i)
        soup = urlToScrap('https://en.wikipedia.org/wiki/' + str(i) + '_Atlantic_hurricane_season')
        scrapFromWiki(i, soup, stormName, datesActive, stormCategory, maxMinWind, minPressure,
                      damageUSD, deaths, year)
    except:
        continue
dataset = pd.DataFrame(
    {'Storm Name': stormName, 'Year': year, 'Dates Active': datesActive, 'Storm Category': stormCategory
        , 'Max min wind': maxMinWind, 'Min Pressures': minPressure
        , 'Damage USD': damageUSD, 'Deaths': deaths})

print(dataset)

print(f"This program take {time.time()-start} seconds")