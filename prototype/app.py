from flask import Flask, render_template

# local
from map_chart import map_chart
from curve_chart import curve_chart
from distribution_chart import distribution_chart


app = Flask(__name__)

@app.route("/")
def hello():
    # map_chart()
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
