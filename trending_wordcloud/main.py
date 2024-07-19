import pandas as pd
import time
import json
import requests
from bs4 import BeautifulSoup


def get_dates():
    dates = pd.date_range('2020-01-01', '2020-12-27', freq='7d')
    dates = [d.strftime('%Y-%m-%d') for d in dates]
    return dates


def get_keywords(date):
    result = {}
    url = f'https://us.trend-calendar.com/trend/{date}.html'
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Failed to get data from {url}")
    soup = BeautifulSoup(r.text, "html.parser")

    # Twitter_trends
    try:
        twitter_trends = soup.find_all('div', class_='readmoretable')[
            0].find_all('div', class_='readmoretable_line')[0:10]
        for idx, trend in enumerate(twitter_trends):
            trend = trend.a.text.lstrip('#').lower()
            result[trend] = result.get(trend, 0) + (10 - idx)
    except Exception as e:
        print(e)
        print(f"Failed to get twitter Hashtags from {url}")

    # Google_trends
    try:
        google_trends = soup.find_all('div', class_='readmoretable')[
            1].find_all('div', class_='readmoretable_line')[0:10]
        for idx, trend in enumerate(google_trends):
            trend = trend.a.text.lstrip('#').lower()
            result[trend] = result.get(trend, 0) + (10 - idx)
    except Exception as e:
        print(e)
        print(f"Failed to get google trends from {url}")
    print(f"Scraped data for {date} successfully")

    return result


start = time.time()
dates_list = get_dates()

keywords = {}
for date in dates_list:
    keywords[date] = get_keywords(date)

print("Dumping into file")
with open('data/weekly.json', 'w') as file:
    json.dump(keywords, file)

duration = time.time() - start
print(f"Scraping completed :) took {duration} seconds")

print("Collecting combined result")

with open('data/weekly.json', 'r') as file:
    keywords = json.load(file)
    combined_result = {}
    for date, week_keyword in keywords.items():
        for keyword in week_keyword:
            combined_result[keyword] = combined_result.get(
                keyword, 0) + week_keyword[keyword]

    print("Dumping into file")
    with open('data/combined.json', 'w') as file:
        json.dump(combined_result, file)
    print(f"Done :D Got {len(combined_result)} keywords")
