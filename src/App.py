from flask import request, render_template
from . import Client


def main(path: str) -> str:
    parameters = request.args
    cookies = request.cookies
    requested_website = ""
    requested_website_param = parameters.get("web_proxy_requested_website")
    requested_website_cookie = cookies.get("web_proxy_requested_website")

    if requested_website_param:
        requested_website = requested_website_param
    elif requested_website_cookie:
        requested_website = requested_website_cookie
    else:
        return render_template("index.html")
    return Client.simple_request(requested_website)
