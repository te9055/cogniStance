from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/ner")
def ner():
    return "Hello ner!"


@app.route("/usas")
def usas():
    return "Hello usas!"
