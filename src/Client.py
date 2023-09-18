from flask import Response, request
import requests


def __transform_query(
    parameters: dict = {}, headers: dict = {}, cookies: dict = {}
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


def __handler_html_css(html_css_file: bytes):
    return html_css_file


def __handler_stream(response: requests.Response, headers: dict):
    html_css_file = b""
    for chunk in response.iter_content(chunk_size=8192):
        if not chunk:
            continue
        if "text/html" in headers.get("Content-Type", None):
            html_css_file += chunk
            continue
        yield chunk
    yield __handler_html_css(html_css_file)


def __handle_response(response: requests.Response) -> Response:
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
    method_assoc = {"GET": requests.get, "POST": requests.post}
    parameters = request.args.to_dict(True)
    cookies = request.cookies.to_dict(True)
    headers = dict(request.headers)
    __transform_query(parameters=parameters, headers=headers, cookies=cookies)
    if not method_assoc.get(request.method, None):
        return Response(status=405)
    method_function = method_assoc[request.method]
    response = method_function(
        url=f"{__website}{request.path}",
        params=parameters,
        cookies=cookies,
        headers=headers,
        data=request.stream,
    )
    return __handle_response(response)
