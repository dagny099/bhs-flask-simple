from app import app
from flask import render_template, request, redirect
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime

#Goal 1:
# Have user input stock ticker symbol
# Plot closing price data for 1 month
#Goal 2:
# add inputs to select Start & End date
#Goal 3:
# add a dropdown with "Closing Price", "Opening Price", "High", "Low", "Volume"
def getStockData(symb, startDate, endDate):
    info = data.DataReader(symb,'stooq',start= startDate,end= endDate)
    print(info)
    return info

@app.route('/')
def index():
  return render_template('public/index.html')

@app.route('/about')
def about():
  return """<h1 style='color: red;'>I'm a red H1 heading!</h1>
  <p>This is some text in a paragraph tag</p>
  <code>Flask is <em>awesome</em></code>
  <a href="/">Home</a>
  """
#  return render_template('public/about.html')

@app.route('/around', methods=["GET", "POST"])
def around():
    if request.method=="POST":
        req = request.form

        #Give feedback if form elements are missing:
        missing = list()
        for k, v in req.items():
            if v =="":
                missing.append(k)
        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template('public/around.html', feedback=feedback)

        #Give feedback if form elements are missing:
        info = getStockData(req["symb"], req["startdate"], datetime.date.today())
        if len(info)==0:
            feedback = f"{symb} Is not a valid stock symbol!"
            return render_template('public/around.html', feedback=feedback)
        else:
            infoSch = f"Stock symbol is: {req['symb']}, Start Date is: {req['startdate']}, and End Date is: {datetime.date.today()}"
            infoMax = f"In that period, the HIGHEST closing was {info['Close'].max()} on {info['Close'].idxmax().strftime('%B %d, %Y')}."
            infoMin = f"In that period, the LOWEST closing was {info['Close'].min()} on {info['Close'].idxmin().strftime('%B %d, %Y')}."
            return render_template('public/around.html', infoTxt=[infoSch, infoMax, infoMin])
    return render_template('public/around.html')

@app.route('/hello/<name>')
def hello_name(name):
  return 'Hello %s!!' % name
