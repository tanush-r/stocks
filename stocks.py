from pandas_datareader import data
from datetime import datetime
import constants
import pandas as pd
import plotly.express as px


def get_graph(tickers, start_date, end_date):
    constants.setup_api_key()
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    stock_data = pd.DataFrame()
    stock_data_tick = pd.DataFrame()

    for tick in tickers:
        stock_data_tick = data.DataReader(tick, "av-daily", start=start_date, end=end_date)
        stock_data[tick] = stock_data_tick["close"]
    stock_data.index = stock_data_tick.index

    fig = px.line(stock_data, x=stock_data.index, y=stock_data.columns, markers=True)

    # fig.update_layout(title='Tech Stocks past 90 Days')
    # fig.update_layout(legend_title_text='Companies')
    fig.write_html("templates\\graph.html")
