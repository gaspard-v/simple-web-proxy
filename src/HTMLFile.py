from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import os


def __find_all_link(soup: BeautifulSoup):
    elements = soup.find_all(True, href=True)
    elements += soup.find_all(True, src=True)
    return elements


def __parse_link(link):
    server_schema = os.environ.get("WEB_PROXY_SCHEMA")
    server_port = os.environ.get("WEB_PROXY_PORT")
    server_netloc = os.environ.get("WEB_PROXY_NETLOC")
    not_standard_port = ("http" in server_schema and server_port != "80") or (
        "https" in server_schema and server_port != "443"
    )
    if server_port and not_standard_port:
        server_netloc += f":{server_port}"
    parsed_link = urlparse(link)
    if parsed_link.scheme == "data":
        return link
    if parsed_link.netloc:
        netloc = parsed_link.netloc
        schema = parsed_link.scheme
        if not schema:
            schema = urlparse(__website).scheme
        new_params = f"web_proxy_requested_website={schema}://{netloc}"
    else:
        new_params = f"web_proxy_requested_website={__website}"
    query_params = parse_qs(parsed_link.query)
    query_params.update(parse_qs(new_params))
    new_query = urlencode(query_params, doseq=True)
    new_link = urlunparse(
        (
            server_schema,
            server_netloc,
            parsed_link.path,
            parsed_link.params,
            new_query,
            parsed_link.fragment,
        )
    )
    return new_link


def __change_links(elements):
    link = ""
    method = ""
    for element in elements:
        if element.get("href", None):
            link = element["href"]
            method = "href"
        elif element.get("src", None):
            link = element["src"]
            method = "src"
        else:
            continue
        new_link = __parse_link(link)
        element[method] = new_link


def __add_js(soup: BeautifulSoup):
    script = soup.new_tag("script")
    with open(
        os.path.join(
            os.path.dirname(__file__), "..", "javascript", "dist", "bundle.js"
        ),
        encoding="utf-8",
    ) as js:
        script.string = js.read()
    first_script = soup.head.find("script")
    if first_script:
        first_script.insert_before(script)
    else:
        soup.head.append(script)


def parse(website: str, html: str):
    global __website
    __website = website
    soup = BeautifulSoup(html, "html5lib")
    elements = __find_all_link(soup)
    __change_links(elements)
    __add_js(soup)
    return soup.prettify()
