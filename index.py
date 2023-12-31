from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from src import App
import os

load_dotenv()

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
cors = CORS(app, origins="*", allow_headers="*", methods=HTTP_METHODS)


@app.route("/", defaults={"path": ""}, methods=HTTP_METHODS)
@app.route("/<path:path>")
def main(path):
    return App.main(path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("WEB_PROXY_PORT"))
