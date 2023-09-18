from flask import Flask
from src import App

app = Flask(__name__, template_folder="src/templates")

HTTP_METHODS = [
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
    "PATCH",
]


@app.route("/", defaults={"path": ""}, methods=HTTP_METHODS)
@app.route("/<path:path>")
def main(path):
    return App.main(path)
