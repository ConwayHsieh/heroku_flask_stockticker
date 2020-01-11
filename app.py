import requests
import simplejson
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

api_key = '.json?api_key=LK-GzNcJMvWfCrxDWsRr'
api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/'

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    ticker = request.form['ticker']
    raw_data = requests.get(api_url + ticker + api_key).json()

    df = pd.DataFrame(raw_data['data'], columns=raw_data['column_names'])
    
    df['Date'] = pd.to_datetime(df['Date'])

    p = figure(title='Stock prices for %s' % ticker,
        x_axis_label='date',
        x_axis_type='datetime')
    
    if request.form.get('Close'):
        p.line(x=df['Date'].values, y=df['Close'].values,line_width=2, \
            line_color = "blue", legend_label='Close')
    if request.form.get('Adj. Close'):
        p.line(x=df['Date'].values, y=df['Adj. Close'].values,line_width=2, \
            line_color="red", legend_label='Adj. Close')
    if request.form.get('Open'):
        p.line(x=df['Date'].values, y=df['Open'].values,line_width=2, \
            line_color="purple", legend_label='Open')
    if request.form.get('Adj. Open'):
        p.line(x=df['Date'].values, y=df['Adj. Open'].values,line_width=2, \
            line_color="orange", legend_label='Adj. Open')
    script, div = components(p)
    return render_template('plot.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

