from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "key"

gifts = []

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        gift = request.form.get("gift")
        if not gift:
            flash("Пустой подарок нельзя добавить!")
            return redirect("/")
        gifts.append(gift)
        flash("Подарок добавлен!")
        return redirect("/")

    search = request.args.get("search")
    if search:
        if search in gifts:
            result = "Такой подарок уже есть в списке"
        else:
            result = "Такого подарка ещё нет в списке"

    return render_template("index.html", gifts=gifts, result=result)

if __name__ == "__main__":
    app.run(debug=True)
