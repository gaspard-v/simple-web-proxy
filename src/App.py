from flask import request, render_template
import requests
from . import Client


def main(path: str) -> str:
    path = request.path
    parameters = request.args
    cookies = request.cookies
    requested_website = ""
    body = request.get_data()
    requested_website_param = parameters.get("web_proxy_requested_website")
    requested_website_cookie = cookies.get("web_proxy_requested_website")

    if requested_website_param:
        requested_website = requested_website_param
    elif requested_website_cookie:
        requested_website = requested_website_cookie
    else:
        return render_template("index.html")
    return Client.simple_request(requested_website)


# from flask import Flask, render_template, Response

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('sse.html')

# # Route SSE
# @app.route('/sse')
# def sse():
#     def event_stream():
#         count = 0
#         while True:
#             yield f"data: {count}\n\n"
#             count += 1

#     return Response(event_stream(), content_type='text/event-stream')

# if __name__ == '__main__':
#     app.run(debug=True)
