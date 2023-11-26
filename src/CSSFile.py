import cssutils
from . import ParseLink


def __change_links(css_obj):
    for rule in css_obj:
        if rule.type != rule.STYLE_RULE:
            continue
        for prop in rule.style:
            if prop.name not in ["background-image", "background"]:
                continue
            url_value = prop.value
            if "url(" not in url_value.lower():
                continue
            url_start = url_value.index("url(") + 4
            url_end = url_value.index(")")
            url = url_value[url_start:url_end].strip("'\"")
            new_link = ParseLink.parse(url, __website)
            new_link = f'url("{new_link}")'
            prop.value = new_link
    return css_obj.cssText


def parse(website: str, css: str | bytes):
    global __website
    __website = website
    return css  # parsing css is very slow ! MUST FIX
    try:
        css_obj = cssutils.parseString(css, validate=False)
        return __change_links(css_obj)
    except:
        return css
