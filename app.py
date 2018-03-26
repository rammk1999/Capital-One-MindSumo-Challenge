# contains all the code for the front end web development

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import predictor
import time

app = Flask(__name__)
Bootstrap(app)


# creates the home page
@app.route("/")
def index():
    return render_template('index.html')


# creates as section of the website that displays the prediction
@app.route("/dispatch_predictor", methods=["GET", "POST"])
def predict_dispatch():
    if request.method == "POST":
        global response

        # receive user input
        input_lat = request.form.get("latitude")
        input_long = request.form.get("longitude")
        user_time = request.form.get("time")

        # check to make sure the time portion was entered properly and proceed accordingly. The latitude and longitude
        # inputs are handled by the template
        try:
            user_time = time.strptime(user_time, "%H:%M:%S")
            # initialize the classifier
            classifier = predictor.DispatchUnitPredictor()
            dispatch_code = classifier.predict_dispatch(user_latitude=float(input_lat),
                                                        user_longitude=float(input_long), user_time=user_time)

            # tuples of the unit_codes and the corresponding unit they're assigned to
            unit_codes = (1, 2, 3, 4, 5, 6, 7, 8, 9)
            units = ("INVESTIGATION", "SUPPORT", "RESCUE SQUAD", "RESCUE CAPTAIN", "CHIEF", "TRUCK",
                     "PRIVATE", "ENGINE", "MEDIC")
            dispatch_prediction = ""

            for code in unit_codes:
                # round the classifier's prediction so it matches one of the unit codes
                if code == int(round(dispatch_code)):
                    # once the proper code is found, assign the unit that code is for
                    dispatch_prediction = units[code - 1]

            # returns the dispatch on a successful prediction
            response = "Dispatch: " + dispatch_prediction

        except ValueError:
            # returns a message if the time is incorrect
            response = "Incorrect time. Re-input your data"

    return render_template('index.html', response=response)


if __name__ == "__main__":
        app.run(debug=True)
