import bs4
import requests


# constants
LAST_YEAR = 2021
FIRST_YEAR = 1851


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


def getStormInformation(stormSoup, ocean, year, years, oceans, dates, times, windPower, airPressure,
                        stormType, stormNames, latCorr, longCorr):
    """
   this function scrap from wunderground web, scrap the measurements of every storm.
    link - https://www.wunderground.com/hurricane/archive
    :param stormSoup: get instance of soup
    :param ocean: get ocean of current storm
    :param year: get year of current storm
    :param years: list of years of storms
    :param oceans: list of oceans of storms
    :param dates: list of date of storms
    :param times: list of time of every single measurement of storm
    :param windPower: list of wind power of every single measurement of storm
    :param airPressure: list of air pressure of every single measurement of storm
    :param stormType: list of storm type of storm
    :param stormNames: list of storms name
    :param latCorr: list of latitude of storms
    :param longCorr: list of longitude of storms
    :return: for now nothing
    """
    stormName = stormSoup.find('td', class_='mat-cell cdk-cell cdk-column-summaryStormName'
                                        ' mat-column-summaryStormName ng-star-inserted').find('a').text
    # If the name of the storm is not-named there is no measurement
    if stormName == 'NOT_NAMED':
        years.append(year)
        oceans.append(ocean)
        dates.append(stormSoup.find('td', class_="mat-cell cdk-cell cdk-column-designatedTrack"
                                             " mat-column-designatedTrack ng-star-inserted")
                     .find('span').text)
        try:
            windPower.append(stormSoup.find('td', class_='mat-cell cdk-cell '
                                                     'cdk-column-highestMaximumSustainedWind '
                                                     'mat-column-highestMaximumSustainedWind'
                                                     ' ng-star-inserted').find('span').text)
        except:
            windPower.append(0)
        try:
            airPressure.append(stormSoup.find('td', class_='mat-cell cdk-cell cdk-column-lowestMinimumPressure'
                                                       ' mat-column-lowestMinimumPressure ng-star-inserted')
                               .find('span').text)
        except:
            airPressure.append(0)

        stormType.append(stormSoup.find('td', class_="mat-cell cdk-cell cdk-column-maximumStormType"
                                                 " mat-column-maximumStormType ng-star-inserted")
                         .find('span').text)
    # else There is measurement
    else:
        stormLink = stormSoup.find('a', href=True)
        soupStorm = urlToScrap(stormLink['href'])
        measurements = soupStorm.find_all('tr', class_='mat-row cdk-row ng-star-inserted')
        for measurement in measurements:
            oceans.append(ocean)
            years.append(year)
            stormNames.appand(stormName)
            dates.append(measurement.find('td', class_='mat-cell cdk-cell cdk-column-date '
                                                       'mat-column-date ng-star-inserted')
                         .find('span').text)
            times.append(measurement.find('td', class_='mat-cell cdk-cell cdk-column-time'
                                                       ' mat-column-time ng-star-inserted')
                         .find('span').text)
            latCorr.append(measurement.find('td', class_='mat-cell cdk-cell cdk-column-lat'
                                                         ' mat-column-lat ng-star-inserted')
                           .find('span').text)
            longCorr.append(measurement.find('td', class_='mat-cell cdk-cell cdk-column-lon'
                                                          ' mat-column-lon ng-star-inserted')
                            .find('span').text)
            try:
                windPower.append(measurement.find('td', class_='mat-cell cdk-cell cdk-column-wind'
                                                               ' mat-column-wind ng-star-inserted')
                                 .find('span').text)
            except:
                windPower.append(0)
            try:
                airPressure.append(measurement.find('td', class_='mat-cell cdk-cell cdk-column-pressure'
                                                                 ' mat-column-pressure ng-star-inserted')
                                   .find('span').text)
            except:
                airPressure.append(0)
            stormType.append(measurement.find('td', class_='mat-cell cdk-cell cdk-column-type'
                                                           ' mat-column-type ng-star-inserted')
                             .find('span').text)


# Crawling from Wunderground
def scrapFromWUnderground(years, oceans, dates, times, windPower, airPressure,
                          stormType, stormNames, latCorr, longCorr):
    """
    this function scrap from wunderground web, scrap every year and than the measurement of every storm.
    link - https://www.wunderground.com/hurricane/archive
    :param years: list of years of storms
    :param oceans: list of oceans of storms
    :param dates: list of date of storms
    :param times: list of time of every single measurement of storm
    :param windPower: list of wind power of every single measurement of storm
    :param airPressure: list of air pressure of every single measurement of storm
    :param stormType: list of storm type of storm
    :param stormNames: list of storms name
    :param latCorr: list of latitude of storms
    :param longCorr: list of longitude of storms
    :return: for now nothing
    """
    # URL and name of the oceans
    oceansURL = {
        'Atlantic Ocean': "https://www.wunderground.com/hurricane/archive/AL",
        'East Pacific': "https://www.wunderground.com/hurricane/archive/EP",
        'Western Pacific': "https://www.wunderground.com/hurricane/archive/WP",
        'Indian Ocean': "https://www.wunderground.com/hurricane/archive/IO",
        'Central Pacific': "https://www.wunderground.com/hurricane/archive/CP",
        'Southern Hemisphere': "https://www.wunderground.com/hurricane/archive/SH"
    }
    for ocean, url in oceansURL:
        soup = urlToScrap(url)
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
        oceans.append(ocean)
        for td in tdOfYear:
            tdStormsNames = soup.find_all('td',
                                          class_='mat-cell cdk-cell cdk-column-summaryStormName'
                                                 ' mat-column-summaryStormName ng-star-inserted')
            toOfMaxWinds = soup.find_all('td',
                                         class_='mat-cell cdk-cell cdk-column-highestMaximumSustainedWind '
                                                'mat-column-highestMaximumSustainedWind ng-star-inserted')
            tdOfMinPressure = soup.find_all('td',
                                            class_='mat-cell cdk-cell cdk-column-lowestMinimumPressure '
                                                   'mat-column-lowestMinimumPressure ng-star-inserted')
            tdOfMaxStrength = soup.find_all('td',
                                            class_='mat-cell cdk-cell cdk-column-maximumStormType '
                                                   'mat-column-maximumStormType ng-star-inserted')
            tdOfDates = soup.find_all('td',
                                      class_='mat-cell cdk-cell cdk-column-designatedTrack '
                                             'mat-column-designatedTrack ng-star-inserted')
        for year in range(FIRST_YEAR, LAST_YEAR):
            soupYear = urlToScrap(url + '/' + year)
            storms = soupYear.find_all('tr', class_='mat-row cdk-row ng-star-inserted')
            for storm in storms:
                getStormInformation(storm, ocean, year, years, oceans, dates, times, windPower, airPressure,
                                    stormType, stormNames, latCorr, longCorr)
