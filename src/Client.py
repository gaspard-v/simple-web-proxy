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
        headers.pop("Accept-Encoding", None)
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


def __handler_html_css(html_css_file: bytes):
    pass


def __handler_stream(response: requests.Response, headers: dict):
    html_css_file = b""
    for chunk in response.iter_content(chunk_size=8192):
        if not chunk:
            continue
        if "text/html" in headers.get("Content-Type", None):
            html_css_file += chunk
            continue
        yield chunk  # TODO: check if the file is HTML or CSS, if not, send without verification
    return __handler_html_css(html_css_file)


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
        stream=True,
    )
    r_headers = dict(response.headers)
    __transform_response(headers=r_headers)
    r_status = response.status_code
    return Response(
        response=__handler_stream(response, r_headers),
        status=r_status,
        headers=r_headers,
    )


def simple_request(website):
    global __website
    __website = website
    method_assoc = {"GET": __get}
    method_function = method_assoc[request.method]
    return method_function()
