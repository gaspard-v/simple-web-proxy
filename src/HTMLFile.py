from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import html5lib


def __find_all_absolute_link(soup: BeautifulSoup):
    elements = soup.find_all(True, href=True)
    elements += soup.find_all(True, src=True)
    # elements += soup.find_all(True, data-src=true)
    # elements += soup.find(["script", "meta", "img"], src=True)
    return elements


def __parse_link(link):
    server_netloc = ""
    server_schema = ""
    parsed_link = urlparse(link)
    if parsed_link.scheme and parsed_link.netloc:
        netloc = parsed_link.netloc
        schema = parsed_link.scheme
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


def parse(website: str, html: str):
    global __website
    __website = website
    soup = BeautifulSoup(html, "html5lib")
    elements = __find_all_absolute_link(soup)
    __change_links(elements)
    return soup.prettify()
