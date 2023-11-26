from bs4 import BeautifulSoup
import os
from . import ParseLink


def __find_all_link(soup: BeautifulSoup):
    elements = soup.find_all(True, href=True)
    elements += soup.find_all(True, src=True)
    return elements


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
        new_link = ParseLink.parse(link, __website)
        element[method] = new_link


def __add_js(soup: BeautifulSoup):
    script = soup.new_tag("script")
    with open(
        os.path.join(
            os.path.dirname(__file__), "..", "javascript", "dist", "main.bundle.js"
        ),
        encoding="utf-8",
    ) as js:
        script.string = js.read()
    first_script = soup.head.find("script")
    if first_script:
        first_script.insert_before(script)
    else:
        soup.head.append(script)


def parse(website: str, html: str | bytes):
    global __website
    __website = website
    soup = BeautifulSoup(html, "html5lib")
    elements = __find_all_link(soup)
    __change_links(elements)
    __add_js(soup)
    return soup.prettify()
