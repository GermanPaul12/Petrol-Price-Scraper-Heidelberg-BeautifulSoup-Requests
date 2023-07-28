import requests
import datetime as dt
import time
import yagmail
import os


def stocks_and_news():
    ALPHA_API_KEY = os.environ['ALPHA_API_KEY']
    NEWS_API_KEY = os.environ['NEWS_API_KEY']
    STOCK_NAME = "AAPL"
    COMPANY_NAME = "Apple"

    STOCK_ENDPOINT = "https://www.alphavantage.co/query"
    NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    stock_parameters = {
        "apikey": ALPHA_API_KEY,
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
    }
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "relevancy",
        "q": COMPANY_NAME,
        "searchIn": "title,description",
    }

    response_stock = requests.get(STOCK_ENDPOINT, params=stock_parameters)
    response_news = requests.get(NEWS_ENDPOINT, params=news_parameters)
    response_stock.raise_for_status()
    response_news.raise_for_status()

    stock_data = response_stock.json()
    news_data = response_news.json()

    today_day = dt.datetime.now().day
    yesterday_day = today_day - 1
    current_month = dt.datetime.now().month
    current_year = dt.datetime.now().year
    last_refreshed = stock_data["Meta Data"]["3. Last Refreshed"]

    yesterday_closing_price = stock_data["Time Series (Daily)"][
        f"{last_refreshed}"]["4. close"]

    last_refreshed_list = last_refreshed.split("-")
    day_before_last_refreshed = int(last_refreshed_list[2]) - 1
    if day_before_last_refreshed < 10:
        last_refreshed_list[2] = f"0{day_before_last_refreshed}"
    else:
        last_refreshed_list[2] = day_before_last_refreshed
    day_before_last_refreshed = "-".join(
        [str(item) for item in last_refreshed_list])

    day_before_yesterday_price = stock_data["Time Series (Daily)"][
        f"{day_before_last_refreshed}"]["4. close"]

    difference = float(yesterday_closing_price) - float(
        day_before_yesterday_price)
    if difference < 0:
        difference = difference * (-1)

    difference_percentage = difference / float(yesterday_closing_price) * 100

    #Append to the csv file
    with open('stock_data.csv', 'a+') as data_file:
        data_file.write(
            f"{yesterday_closing_price},{day_before_yesterday_price},{difference_percentage}"
        )

    if True:
        titles = []
        descriptions = []
        urls = []
        for _ in range(3):
            titles.append(news_data["articles"][_]["title"])
            descriptions.append(news_data["articles"][_]["description"])
            urls.append(news_data["articles"][_]["url"])

    for _ in range(3):
        sender = yagmail.SMTP(os.environ['GMAIL_MAIL'], os.environ['EMAIL_PW'])
        sender.send(to=os.environ['OUTLOOK_MAIL'],
                    subject=f"{titles[_]}",
                    contents=f"{descriptions[_]}\n\nURL: {urls[_]}")
