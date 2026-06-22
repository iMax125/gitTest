from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

menu = {
    "Капучино": 80,
    "Лате": 85,
    "Еспресо": 60,
    "Чізкейк": 120,
    "Панкейки": 95
}

@app.route("/")
def index():
    now = datetime.now()
    current_hour = now.hour
    return render_template("index.html", hour=current_hour)

@app.route("/menu")
def menu_page():
    now = datetime.now()
    weekday = now.strftime("%A")
    return render_template("menu.html", weekday=weekday, menu=menu)

if __name__ == "__main__":
    app.run(debug=True)
