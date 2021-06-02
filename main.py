from flask import render_template,redirect,request,Blueprint
from flask_login import login_required,current_user
main = Blueprint("main",__name__)

@main.route("/")
def home():

    return render_template("home.html")

@main.route("/profile")
@login_required
def profile():

    return render_template("profile.html", user = current_user)