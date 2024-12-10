from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", title="Page d'accueil")


@app.route("/login")
def login():
    return render_template("auth/login.html", title="Page de connexion")


@app.route("/register")
def register():
    return render_template("auth/register.html", title="Page d'inscription")
