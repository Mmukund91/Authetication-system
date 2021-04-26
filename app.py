from flask import Flask
from flask import render_template

app = Flask(__name__, instance_relative_config=True)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()



