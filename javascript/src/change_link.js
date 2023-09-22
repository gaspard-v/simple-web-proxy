import get_parameter_by_name from "./get_parameter";
import get_cookie from "./get_cookie";
const absolute_to_relatif = (link) => {
    if (!link.startsWith(window.location.href)) return link;
    return link.slice(window.location.href.length);
};

const change_link = (link) => {
    try {
        const url = new URL(link);
        const base_url = new URL(window.location.href);
        if (url.protocol === "data:") return link;
        const origin = url.origin;
        const params = url.searchParams;
        if (params.get("web_proxy_requested_website")) return link;
        let new_origin = origin;
        if (origin == base_url.origin) {
            const cookie = get_cookie("web_proxy_requested_website");
            if (cookie) new_origin = cookie;
            else {
                const param = get_parameter_by_name(
                    "web_proxy_requested_website",
                );
                new_origin = param;
            }
        }
        params.append("web_proxy_requested_website", new_origin);
        url.host = base_url.host;
        url.protocol = base_url.protocol;
        url.search = params;
        return url.toString();
    } catch (error) {
        return link;
    }
};

export default change_link;
