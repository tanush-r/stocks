from flask import Flask, render_template, request, url_for, redirect
import json
import stocks

app = Flask(__name__)


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/graph')
def graph():
    return render_template('graph.html')


@app.route('/graph_page')
def graph_page():
    graph_json = request.args.get("graph_json")
    error = request.args.get("error")
    if error is None:
        error = False
    return render_template('graph_page.html', graph_json=graph_json, error=error)


@app.route('/new', methods=['POST'])
def new():
    tick = request.form['ticker']
    from_date = request.form['from-date']
    to_date = request.form['to-date']

    stocks_obj = stocks.stocks(tick, from_date, to_date)
    stocks_obj.main()
    return redirect(url_for('graph_page', graph_json=stocks_obj.graph_json, error=stocks_obj.error))


if __name__ == '__main__':
    app.run(debug=True)
