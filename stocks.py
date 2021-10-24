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
        if not self.tick and not self.start_date and not self.end_date:
            self.error = "Empty data"
            return False
        constants.setup_api_key()
        self.string_to_datetime()
        return True

    def check_date_error(self):
        if self.start_date >= self.end_date:
            self.error = "Wrong date range."
        elif self.start_date > self.today_date or self.end_date > self.today_date:
            self.error = "Date should not be later than today."

    def string_to_datetime(self):
        try:
            self.end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            self.start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        except ValueError:
            self.error = "Wrong date format"

    def datetime_to_string(self):
        self.end_date = self.end_date.strftime('%d %B, %Y')
        self.start_date = self.start_date.strftime('%d %B, %Y')

    def graph(self):
        try:
            stock_data = data.DataReader(self.tick, "av-daily", start=self.start_date, end=self.end_date)[["close"]]
            fig = px.line(stock_data, x=stock_data.index, y=stock_data.columns, color_discrete_sequence=["#77DD77"])
            fig.update_layout(template="plotly_dark", showlegend=False)
            fig.update_yaxes(title_text="Close ($)")
            self.datetime_to_string()
            fig.update_layout(title='%s Stocks from %s to %s.' % (self.tick, self.start_date, self.end_date))
            self.graph_json = json.dumps(fig, cls=utils.PlotlyJSONEncoder)
        except ValueError:
            self.error = "Wrong Ticker value"
            self.graph_json = ""

    def main(self):
        check = self.setup()
        if check:
            self.check_date_error()
            if not self.error:
                self.graph()
            else:
                self.graph_json = ""
        else:
            self.graph_json = ""
