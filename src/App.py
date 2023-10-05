from flask import request, render_template
from . import Client
import os
from urllib.parse import urlparse


def main(path: str) -> str:
    parameters = request.args.to_dict(True)
    requested_website = urlparse(request.base_url)
    requested_website = requested_website.hostname
    requested_website = requested_website.replace(
        os.environ.get("WEB_PROXY_NETLOC"), ""
    )
    if not requested_website:
        return render_template("index.html")
    requested_website = requested_website[:-1]
    port = parameters.get("web_proxy_port", None)
    method = parameters.get("web_proxy_method", None)
    if port:
        requested_website = f"{requested_website}:{port}"
    if method:
        requested_website = f"{method}://{requested_website}"
    else:
        requested_website = f"http://{requested_website}"
    return Client.simple_request(requested_website)
