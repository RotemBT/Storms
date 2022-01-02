from AcquisitionHelper import *

start = time.time()
stormName = []
datesActive = []
stormCategory = []
maxMinWind = []
minPressure = []
damageUSD = []
deaths = []
year = []
for i in range(FIRST_YEAR, LAST_YEAR):
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

print(f"This program take {time.time() - start} seconds")
