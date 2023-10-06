from . import Base36
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import os


def parse(link, website):
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
    if server_netloc in parsed_link.netloc:
        return link
    query_params = parse_qs(parsed_link.query)
    if parsed_link.netloc:
        netloc = parsed_link.netloc
        schema = parsed_link.scheme
        port = parsed_link.port
    else:
        website_url = urlparse(website)
        netloc = website_url.netloc
        schema = website_url.scheme
        port = website_url.port
    if schema:
        query_params.update(parse_qs(f"web_proxy_method={schema}"))
    if port:
        query_params.update(parse_qs(f"web_proxy_port={port}"))
    netloc = Base36.encode(netloc)
    server_netloc = f"{netloc}.{server_netloc}"

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
