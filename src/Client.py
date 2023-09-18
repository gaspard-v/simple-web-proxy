from flask import Response, request
import requests


def __transform_query(
    parameters: dict = None, headers: dict = None, cookies: dict = None
) -> None:
    if parameters:
        parameters.pop("web_proxy_requested_website", None)
    if headers:
        headers.pop("Host", None)
        headers["Referrer"] = __website
    if cookies:
        cookies.pop("web_proxy_requested_website", None)


def __transform_response(headers: dict = None) -> None:
    keys = ["Content-Type", "Set-Cookie"]
    header_normalized = {key.lower(): value for key, value in headers.items()}
    keys_normalized = [key.lower() for key in keys]
    r_headers = {}
    for i in range(len(keys)):
        key = keys[i]
        key_normalized = keys_normalized[i]
        value = header_normalized.get(key_normalized, None)
        if value:
            r_headers[key] = value
    headers.clear()
    headers.update(r_headers)

    # headers.pop("Connection", None)
    # headers.pop("Transfer-Encoding", None)
    # headers.pop("Content-Length", None)
    # headers.pop("Server", None)
    # headers.pop("Date", None)
    # headers.pop("Strict-Transport-Security", None)


def __get() -> Response:
    params = request.args.to_dict(True)
    cookies = request.cookies.to_dict(True)
    headers = dict(request.headers)
    __transform_query(parameters=params, headers=headers, cookies=cookies)
    response = requests.get(
        url=f"{__website}{request.path}",
        params=params,
        cookies=cookies,
        headers=headers,
    )
    r_headers = dict(response.headers)
    __transform_response(headers=r_headers)
    r_status = response.status_code
    r_content = response.content  # check if the content is gziped or not
    return Response(response=r_content, status=r_status, headers=r_headers)


def simple_request(website):
    global __website
    __website = website
    method_assoc = {"GET": __get}
    method_function = method_assoc[request.method]
    return method_function()
