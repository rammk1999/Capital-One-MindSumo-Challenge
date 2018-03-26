# contains all the code for the front end web development

from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
import csv
import predictor
import time

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/dispatch_predictor", methods=["GET", "POST"])
def predict_dispatch():
    if request.method == "POST":
        global response
        input_lat = request.form.get("latitude")
        input_long = request.form.get("longitude")
        user_time = request.form.get("time")
        try:
            user_time = time.strptime(user_time, "%H:%M:%S")
            classifier = predictor.DispatchUnitPredictor()
            dispatch_code = classifier.predict_dispatch(user_latitude=float(input_lat),
                                                        user_longitude=float(input_long), user_time=user_time)
            print(dispatch_code)
            unit_codes = (1, 2, 3, 4, 5, 6, 7, 8, 9)
            units = ("INVESTIGATION", "SUPPORT", "RESCUE SQUAD", "RESCUE CAPTAIN", "CHIEF", "TRUCK",
                     "PRIVATE", "ENGINE", "MEDIC")
            most_likely_dispatch = "unit"
            for code in unit_codes:
                if code == int(round(dispatch_code)):
                    print(code)
                    most_likely_dispatch = units[code - 1]

            response = "Dispatch: " + most_likely_dispatch

        except ValueError:
            response = "Incorrect time. Re-input your data"

    return render_template('index.html', response=response)


if __name__ == "__main__":
        app.run(debug=True)
