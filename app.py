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


@app.route("/", methods=["GET", "POST"])
def predict_dispatch():
    # add more code here to predict the unit type that is dispatched
    if request.method == "POST":
        input_lat = request.form.get("latitude")
        input_long = request.form.get("longitude")
        user_time = request.form.get("time")
        classifier = predictor.DispatchUnitPredictor()
        most_likely_dispatch = classifier.predict_dispatch(user_latitude=float(input_lat),
                                                           user_longitude=float(input_long), user_time=user_time)
        print(most_likely_dispatch)
        return render_template('index.html', response=most_likely_dispatch)


if __name__ == "__main__":
    app.run(debug=True)
