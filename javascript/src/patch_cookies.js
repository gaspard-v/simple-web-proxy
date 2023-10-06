const check_domain = (full_domaine, partial_domain) =>
    full_domaine.toLowerCase().endsWith(partial_domain.toLowerCase());

const parse_cookie = (cookie_string) => {
    const cookie_obj = {};
    const cookie_parts = cookie_string.split(";");
    const valid_properties = [
        "secure",
        "domain",
        "path",
        "expires",
        "samesite",
    ];

    let idx = 0;
    for (const part of cookie_parts) {
        const [key, value] = part.trim().split("=");
        const lower_key = key.toLowerCase();
        if (idx === 0) {
            cookie_obj["key"] = key;
            cookie_obj["value"] = value;
        }
        if (valid_properties.includes(lower_key)) cookie_obj[lower_key] = value;
        idx++;
    }
    return cookie_obj;
};
const serialize_cookie = (cookie_obj) => {
    let cookie_string = `${cookie_obj.key}=${cookie_obj.value};`;
    for (const key in cookie_obj) {
        const value = cookie_obj[key];
        if (key === "key" || key === "value") continue;
        if (!value) {
            cookie_string += ` ${key};`;
            continue;
        }
        cookie_string += ` ${key}=${value};`;
    }
    return cookie_string;
};
const change_cookie = (cookie_string) => {
    const cookie_obj = parse_cookie(cookie_string);
    const cookie_domain = cookie_obj.domain;
    if (cookie_domain) delete cookie_domain.domain;
    return serialize_cookie(cookie_obj);
};
const patch_cookie = () => {
    const cookieDesc =
        Object.getOwnPropertyDescriptor(Document.prototype, "cookie") ||
        Object.getOwnPropertyDescriptor(HTMLDocument.prototype, "cookie");
    if (!cookieDesc || !cookieDesc.configurable) {
        return;
    }
    Object.defineProperty(document, "cookie", {
        get: function () {
            return cookieDesc.get.call(document);
        },
        set: function (val) {
            val = change_cookie(val);
            cookieDesc.set.call(document, val);
        },
    });
};
export default patch_cookie;
