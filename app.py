# contains all the code for the front end web development

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def index():
    return render_template("index.html")
# https://www.youtube.com/watch?v=t24ZOk06wa8 (part 6)
# https://www.youtube.com/watch?v=AOboS0RESt4 (part 7)
# @app.route("/")
# @app.route("/<user>")
# def index(user=None):
#     return render_template("user.html", user=user)
#
#
# @app.route("/shopping")
# def shopping():
#     food = ["cheese", "Tuna", "Beef", "Toothpaste"]
#     return render_template("shopping.html", food=food)
#
#
# https://www.youtube.com/watch?v=WxgYYGxoPwY
# @app.route("/profile/<name>")
# def profile(name):
#     return render_template("profile.html", name=name)
#
#
# https://www.youtube.com/watch?v=t3yHNZhSXLE
# @app.route("/profile/<name>")
# def profile(name):
#     return render_template("profile.html", name=name)
#
#
# https://www.youtube.com/watch?v=PWF_WyvgKqY
# @app.route('/broccoli', methods=['GET', 'POST'])
# def broccoli():
#     if request.method == 'POST':
#         return "You are using POST"
#     else:
#         return "You are prolly using GET"
#
#
#
# https://www.youtube.com/watch?v=27Fjrlx4s-o
# @app.route('/jayasri')
# def jayasri():
#     return "<h1>Jayasri is my mother</h1>"
#
#
# @app.route('/person/<lovedOne>')
# def person(lovedOne):
#     return "<h1>Hey there %s<h1>" % lovedOne
#
#
# # MUST SPECIFY DATA TYPE IF NOT USING A STRING
# @app.route('/person/<int:id_number>')
# def show_person(id_number):
#     return "<h1>Hey there %s<h1>" % id_number
#
#
# https://www.youtube.com/watch?v=ZVGwqnjOKjk
# # @ signifies a decorator - way to wrap a function and modifying its behavior
# @app.route('/')
# def index():
#     return "<h1>Homepage</h1>"


if __name__ == "__main__":
    app.run(debug=True)
