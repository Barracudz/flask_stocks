from flaskstocks import app
from flask import render_template, url_for, redirect, flash, request, abort
from flaskstocks.forms import StocksForm
import pandas as pd
from matplotlib.figure import Figure
from io import BytesIO
import base64
import pandas_datareader.data as web
import datetime as dt
import numpy as np
import string, random

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = StocksForm()
    # If form is valid, get stock data
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        stocks = [form.stock1.data, form.stock2.data, form.stock3.data, form.stock4.data, form.stock5.data]
        img = getStockData(stocks_chosen=stocks, start=start_date, end=end_date)
        return render_template("home.html", img=img, form=form)
    return render_template("home.html", form=form)

def testPlot():
    fig = Figure()
    ax1, ax2 = fig.subplots(2, sharex=True)
    x = [1, 2, 4]
    y = [2, 8, 5]
    ax1.plot(x, y)
    ax2.plot(y, x)
    # Save plot as png to static/plots folder
    fig.savefig("flaskstocks/static/plots/stocks_plot.png", format='png')
    # Get the image and return it
    img = url_for('static', filename='plots/stocks_plot.png')
    return img

# Function to retrieve and plot data about given stocks
def getStockData(start, end, stocks_chosen):
    stocks = stocks_chosen
    # Filter away empty strings
    stocks = list(filter(lambda a: a != '', stocks))
    print(stocks)
    start = start
    end = end
    currentDate = dt.datetime.today()
    earliestDate = '1900-01-01' # If user wants earliest date

    dfs = [] # Get data from Yahoo and create dataframe
    for s in stocks:
        dfs.append(web.DataReader(s, 'yahoo', start if start != '' else earliestDate, end if end != '' else currentDate))

    marketCapDf = web.get_quote_yahoo(stocks)['sharesOutstanding'] # Get amount of shares

    # Put shares in list
    shares = []
    for i in range(len(stocks)):
        shares.append(marketCapDf.iloc[i])

    # Calculate historical market cap and put dfs in list
    historicalCaps = []
    for i in range(len(stocks)):
        historicalCaps.append(dfs[i]['Close'] * shares[i])

    fig = Figure()
    # Create 3 subplots with shared x-axis
    ax1, ax2, ax3 = fig.subplots(3, sharex=True)

    stocksStr = '' # Create string with tickers
    for s in stocks:
        if s == stocks[len(stocks)-1]:
            stocksStr += s
        else:
            stocksStr += s + ', '

    # Plot chart for historical market cap
    for i in range(len(stocks)):
        ax1.plot(historicalCaps[i])

    ax1.set(ylabel='Market cap in USD')
    ax1.set_title(f'Historical market caps for: {stocksStr}')
    ax1.legend(stocks)

    # Plot chart for historical stock price
    for i in range(len(stocks)):
        ax2.plot(dfs[i]['Close'])

    ax2.set(ylabel='Stock price in USD')
    ax2.set_title(f'Historical stock prices for: {stocksStr}')
    ax2.legend(stocks)

    # Plot chart for percentage growth in stock price
    for i in range(len(stocks)):
        startingPrice = dfs[i].iloc[0][0] # Get startingPrice
        print(f'\nStock: {stocks[i]}')
        print(f'Starting price: {startingPrice}')
        ax3.plot(((dfs[i]['Close'] / startingPrice) - 1) * 100)

    ax3.set(ylabel='Percentage growth')
    ax3.set_title(f'Percentage growth in stock prices of: {stocksStr}')
    ax3.tick_params(axis='x', rotation=70)
    ax3.legend(stocks)
    fig.tight_layout()

    # Generate random file name. Necessary so that cached image is not constantly shown
    file_name = ''.join(random.choice(string.ascii_letters) for i in range(10))
    print(file_name)
    # Save plot as png to static/plots folder
    fig.savefig(f'flaskstocks/static/plots/{file_name}.png', format='png')
    # Get the image and return it
    img = url_for('static', filename=f'plots/{file_name}.png')
    return img
