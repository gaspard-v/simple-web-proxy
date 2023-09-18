from flask import Flask, request
from src import App

app = Flask(__name__, template_folder="src/templates")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def main(path):
    return App.main(path)
