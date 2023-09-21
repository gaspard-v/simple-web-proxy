from flask import Response, request, escape
from . import HTMLFile
import requests
import http.cookies
import os
from urllib.parse import urlparse


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


def __transform_cookies(cookies: str):
    cookies_obj = http.cookies.SimpleCookie(cookies)
    cookies_ret = http.cookies.SimpleCookie()
    domaine = urlparse(__website).netloc
    for cookie in cookies_obj.values():
        key = f"{domaine}_{cookie.key}"
        cookies_ret[key] = cookie.value
        cookies_ret[key]["domain"] = os.environ.get("WEB_PROXY_NETLOC")
        cookies_ret[key]["expires"] = cookie["expires"]
        cookies_ret[key]["path"] = cookie["path"]
        cookies_ret[key]["httponly"] = cookie["httponly"]
        cookies_ret[key]["secure"] = cookie["secure"]
    return cookies_ret.output()


def __transform_response(headers: dict = None) -> None:
    keys = ["Content-Type"]
    header_normalized = {key.lower(): value for key, value in headers.items()}
    keys_normalized = [key.lower() for key in keys]
    r_headers = {}
    for i in range(len(keys)):
        key = keys[i]
        key_normalized = keys_normalized[i]
        value = header_normalized.get(key_normalized, None)
        if not value:
            continue
        r_headers[key] = value
    if header_normalized.get("set-cookie", None):
        lol = __transform_cookies(header_normalized["set-cookie"])
        # TODO: add cookies to client response

    headers.clear()
    headers.update(r_headers)


def __handler_html_css(html_css_file: bytes):
    return HTMLFile.parse(__website, html_css_file)


def __handler_stream(response: requests.Response, headers: dict):
    html_css_file = b""
    for chunk in response.iter_content(chunk_size=8192):
        if not chunk:
            continue
        if "text/html" in headers.get("Content-Type", None):
            html_css_file += chunk
            continue
        yield chunk
    if html_css_file:
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
    method_assoc = {
        "GET": requests.get,
        "POST": requests.post,
        "HEAD": requests.head,
        "PUT": requests.put,
        "PATCH": requests.patch,
        "DELETE": requests.delete,
        "OPTIONS": requests.options,
    }
    parameters = request.args.to_dict(True)
    cookies = request.cookies.to_dict(True)
    headers = dict(request.headers)
    __transform_query(parameters=parameters, headers=headers, cookies=cookies)
    if not method_assoc.get(request.method, None):
        return Response(status=405)
    method_function = method_assoc[request.method]
    try:
        response = method_function(
            url=f"{__website}{request.path}",
            params=parameters,
            cookies=cookies,
            headers=headers,
            data=request.get_data(),  # TODO check why only get_data() works
            verify=False,
        )
    except Exception as err:
        response = f"<p>{escape(err)}</p>"  # TODO use templates
        return Response(response=response, status=500)
    return __handle_response(response)
