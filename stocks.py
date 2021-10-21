from pandas_datareader import data
from datetime import datetime
import constants
import json
from plotly import utils
import plotly.express as px


def get_graph(tick, start_date_str, end_date_str):
    #Set error, error message and add to final json, ciao
    constants.setup_api_key()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    today_date = datetime.today()
    error = dict()
    if start_date >= end_date:
        error["PRS-1"] = "Wrong date range"
        graph_json = json.dumps(error)
        return graph_json
    if start_date > today_date or end_date > today_date:
        error["PRS-2"] = "Date should not be later than today"
        graph_json = json.dumps(error)
        return graph_json
    stock_data = data.DataReader(tick, "av-daily", start=start_date, end=end_date)[["close"]]

    fig = px.line(stock_data, x=stock_data.index, y=stock_data.columns)
    fig.update_layout(template="plotly_dark", showlegend=False)
    fig.update_yaxes(title_text="Close ($)")
    # fig.update_layout(markers=true)
    fig.update_layout(title='%s Stocks from %s to %s' % (tick, start_date_str, end_date_str))
    # fig.update_layout(legend_title_text='Companies')
    graph_json = json.dumps(fig, cls=utils.PlotlyJSONEncoder)
    return graph_json
    # fig.write_html("templates\\graph.html")
