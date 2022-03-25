import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


def get_weather(year=2022, month=1, day=1, location="Mantova"):
    url = 'https://www.ilmeteo.it/portale/archivio-meteo/' + location + '/' \
          + str(year) + '/' + month + '/' + str(day)

    # return response status code
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        # get all table inside soup object
        table = soup.find_all('table')
        raw_data = [row.text.splitlines() for row in table]

        raw_data = raw_data[3]
        # 2 - > temperatura media, 3 -> temperatura minima, 4 -> temperatura massima
        med_temp = raw_data[2].split("media", 1)[1]
        min_temp = raw_data[3].split("minima", 1)[1]
        max_temp = raw_data[4].split("massima", 1)[1]

        # get weather condition
        weather_condition = raw_data[17].split("Meteo", 1)[1]
        # get phenomenon, es. pioggia
        phenomenon = raw_data[16].split("Fenomeni", 1)[1]
        return [phenomenon, weather_condition, min_temp, med_temp, max_temp]
    except:
        print("year: {}, month: {}, day: {}".format(year, month, day))
        return ""


month_names = ["", "Gennaio", "Febbraio", "Marzo",
               "Aprile", "Maggio", "Giugno", "Luglio",
               "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

cities = ["Bergamo", "Roncadelle", "Bolzano", "San Giovanni Teatino",
          "Mondovì", "Como", "Cremona", "Milano", "Mantova", "Piacenza", "Padova", "Pisa", "Roma",
          "Sarzana", "Trento", "Rovereto", "Settimo Torinese", "Muggia", "Udine", "Mestre",
          "Marcon", "Verona", "Zanè"]

dates = pd.date_range(start='1/02/2020', end='20/03/2022', freq='D')
weather_list = []

start_time = time.time()
for city in cities:
    for date in dates:
        weather = get_weather(date.year, month_names[date.month], date.day, city)
        if weather != "":
            weather_list.append([
                date.year,
                date.month,
                date.day,
                weather[0],
                weather[1],
                weather[2],
                weather[3],
                weather[4],
                city
            ])


    print("--- %s seconds ---" % (time.time() - start_time))
    print(city)

    df = pd.DataFrame(weather_list, columns=['year', 'moth', 'day', 'phenomenon', 'weather_condition',
                                             "min_temp", "med_temp", "max_temp", "city"])
    # Save in csv
    df.to_csv(city+'_meteo.csv', index=False)
