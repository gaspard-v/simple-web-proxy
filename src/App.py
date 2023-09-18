from flask import request
import requests


def main(path: str) -> str:
    path = request.path
    parameters = request.args
    cookies = request.cookies
    requested_website = ""
    requested_website_param = parameters.get("web_proxy_requested_website")
    requested_website_cookie = cookies.get("web_proxy_requested_website")

    if requested_website_param:
        requested_website = requested_website_param
        parameters.pop("web_proxy_requested_website")
    elif requested_website_cookie:
        requested_website = requested_website_cookie
        cookies.pop("web_proxy_requested_website")
    else:
        return "TODO: faire la fonction par default"
    return "non"


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
