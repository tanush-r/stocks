from pandas_datareader import data
from datetime import datetime
import constants
import json
from plotly import utils
import plotly.express as px


class stocks:
     
    def __init__(self, tick, start_date, end_date):
        self.tick = tick
        self.start_date = start_date
        self.end_date = end_date
        self.error = ""
        self.graph_json = ""
        self.today_date = datetime.today()

    def setup(self):
        constants.setup_api_key()
        self.end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        self.start_date = datetime.strptime(self.start_date, '%Y-%m-%d')

    def check_date_error(self):
        if self.start_date >= self.end_date:
            self.error = "Wrong date range"
        elif self.start_date > self.today_date or self.end_date > self.today_date:
            self.error = "Date should not be later than today"

    def graph(self):
        try:
            stock_data = data.DataReader(self.tick, "av-daily", start=self.start_date, end=self.end_date)[["close"]]
            fig = px.line(stock_data, x=stock_data.index, y=stock_data.columns)
            fig.update_layout(template="plotly_dark", showlegend=False)
            fig.update_yaxes(title_text="Close ($)")
            # fig.update_layout(markers=true)
            fig.update_layout(title='%s Stocks from %s to %s' % (self.tick, self.start_date, self.end_date))
            # fig.update_layout(legend_title_text='Companies')
            self.graph_json = json.dumps(fig, cls=utils.PlotlyJSONEncoder)
        except ValueError:
            self.error = "Wrong Ticker value"
            self.graph_json = ""

    def main(self):
        self.setup()
        self.check_date_error()
        if not self.error:
            self.graph()
        else:
            self.graph_json = ""
