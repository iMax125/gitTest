from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/temperature", methods=["GET", "POST"])
def temperature():
    c = None
    f = None

    if request.method == "POST":
        c = float(request.form["celsius"])
        f = c * 9/5 + 32

    return render_template("temperature.html", c=c, f=f)

if __name__ == "__main__":
    app.run(debug=True)
