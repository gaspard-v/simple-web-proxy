from flask import request, render_template, abort
from . import Client
import os
from urllib.parse import urlparse
from . import Base36


def main(path: str) -> str:
    parameters = request.args.to_dict(True)
    requested_website = urlparse(request.base_url)
    requested_website = requested_website.hostname
    requested_website = requested_website.replace(
        os.environ.get("WEB_PROXY_NETLOC"), ""
    )
    if not requested_website:
        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "javascript", "dist", "front.bundle.js"
            ),
            encoding="utf-8",
        ) as js:
            return render_template("index.html", js_front_script=js.read())
    requested_website = requested_website[:-1]
    try:
        requested_website = Base36.decode(requested_website)
    except:
        abort(400)
    port = parameters.get("web_proxy_port", None)
    method = parameters.get("web_proxy_method", None)
    if port:
        requested_website = f"{requested_website}:{port}"
    if method:
        requested_website = f"{method}://{requested_website}"
    else:
        requested_website = f"https://{requested_website}"
    return Client.simple_request(requested_website)
