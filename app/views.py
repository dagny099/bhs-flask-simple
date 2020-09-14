from app import app
from flask import render_template, request, redirect
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.embed import components

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

def create_line_graph(info, req):
    source = ColumnDataSource(info)
    # instantiating the figure object
    graph = figure(
        title = f"{req['symb']} Closing Price",
        plot_width=800, plot_height=300,
        x_axis_type='datetime',
        x_axis_label = 'Date',
        y_axis_label = 'US Dollars',
        outline_line_color="#666666"
    )
    # plotting the graph
    graph.line(
        source.data['Date'],
        source.data['Close'],
        line_color = 'maroon',
        line_width=3
    )
    graph.yaxis.formatter=NumeralTickFormatter(format="$0")
    return graph

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
        #Create bokeh line graph
        graph = create_line_graph(info,req)
        # For more details see:
        #   http://bokeh.pydata.org/en/latest/docs/user_guide/embedding.html#components
        script, div = components(graph)
        if len(info)==0:
            feedback = f"{symb} Is not a valid stock symbol!"
            return render_template('public/around.html', feedback=feedback)
        else:
            infoSch = f"Stock symbol is: {req['symb']}, Start Date is: {req['startdate']}, and End Date is: {datetime.date.today()}"
            infoMax = f"In that period, the HIGHEST closing was {info['Close'].max()} on {info['Close'].idxmax().strftime('%B %d, %Y')}."
            infoMin = f"In that period, the LOWEST closing was {info['Close'].min()} on {info['Close'].idxmin().strftime('%B %d, %Y')}."
            return render_template(
                'public/around.html',
                infoTxt=[infoSch, infoMax, infoMin],
                the_div=div, the_script=script,
                req = req)
    return render_template('public/around.html')

@app.route('/hello/<name>')
def hello_name(name):
  return 'Hello %s!!' % name
