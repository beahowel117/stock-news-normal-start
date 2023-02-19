import requests
from twilio.rest import Client

TWILIO_SID = 'AC3a32b779a0b2a35e464c8b2acdb6c675'
TWILIO_AUTH_TOKEN = 'a4dca0628b7666c33d647abbbe7d0e5a'
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = 'C6SO2ZKTG5OF8ZCS'
NEWS_API_KEY = '0ebf0a9691444d2e8a83692206acad45'

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}


## Use https://www.alphavantage.co/documentation/#daily
# https://newsapi.org/
## Use twilio.com/docs/sms/quickstart/python
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#Get yesterday's closing stock price.list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_price = data_list[1]["4. close"]
print(day_before_yesterday_price)

price_diff = float(yesterday_closing_price) - float(day_before_yesterday_price)
up_down = None
if price_diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


diff_percent = round((price_diff /float(yesterday_closing_price)) * 100)
print(diff_percent)

if abs(diff_percent) > 1:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_articles = news_response.json()["articles"]
    three_articles = news_articles[:3]


    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}% \nHeadline: {article['title']}.\nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+18777489136',
            to='+18124317791'
        )

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

