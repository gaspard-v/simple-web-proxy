from flask import Response, request
import requests


def _get(website: str) -> Response:
    params = request.args.to_dict(True)
    params.pop("web_proxy_requested_website", None)
    cookies = request.cookies.to_dict(True)
    cookies.pop("web_proxy_requested_website", None)
    headers = dict(request.headers)
    headers.pop("Host", None)
    headers["Referrer"] = website
    response = requests.get(
        url=f"{website}{request.path}",
        params=params,
        cookies=cookies,
        headers=headers,
    )
    r_headers = dict(response.headers)
    r_headers.pop("Connection", None)
    r_headers.pop("Transfer-Encoding", None)
    r_headers.pop("Content-Length", None)
    r_headers.pop("Server", None)
    r_headers.pop("Date", None)
    r_headers.pop("Strict-Transport-Security", None)
    r_status = response.status_code
    r_content = response.content
    return Response(response=r_content, status=r_status, headers=r_headers)


def simple_request(website):
    method_assoc = {"GET": _get}
    method_function = method_assoc[request.method]
    return method_function(website)
