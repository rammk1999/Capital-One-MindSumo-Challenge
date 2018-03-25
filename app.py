# contains all the code for the front end web development

from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
import csv
import predictor
import datetime

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/", methods=["POST"])
def predict_dispatch():
    # add more code here to predict the unit type that is dispatched
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
