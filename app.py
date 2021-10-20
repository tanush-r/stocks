from flask import Flask, render_template, request, url_for, redirect
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
    return render_template('graph_page.html')


@app.route('/new', methods=['POST'])
def new():
    tick = request.form['ticker']
    from_date = request.form['from-date']
    to_date = request.form['to-date']
    ticks = list()
    ticks.append(tick)
    stocks.get_graph(ticks, from_date, to_date)
    return redirect(url_for('graph_page'))


if __name__ == '__main__':
    app.run(debug=True)
