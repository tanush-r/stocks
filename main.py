from pandas_datareader import data
import datetime
import constants
import pandas as pd
import plotly.express as px


constants.setup_api_key()
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=90)
tickers = "GOOG AMZN AAPL FB MSFT".split(" ")

stock_data = pd.DataFrame()
stock_data_tick = pd.DataFrame()

for tick in tickers:
    stock_data_tick = data.DataReader(tick, "av-daily", start=start_date, end=end_date)
    stock_data[tick] = stock_data_tick["close"]
stock_data.index = stock_data_tick.index

fig = px.line(stock_data, x=stock_data.index, y=stock_data.columns, markers=True)

fig.update_layout(title='Tech Stocks past 90 Days')
fig.update_layout(legend_title_text='Companies')
fig.write_html("res\\graph.html")
