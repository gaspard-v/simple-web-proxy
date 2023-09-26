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
        if (url.host.endsWith("xosh.fr"))
            // TODO: change the link !!!!!!
            // use environment variable
            return link;

        const params = url.searchParams;
        params.append("web_proxy_method", url.protocol.slice(0, -1));
        params.append("web_proxy_port", url.port);
        url.host = `${url.host}.${base_url.host}`;
        url.protocol = base_url.protocol;
        url.search = params;
        return url.toString();
    } catch (error) {
        return link;
    }
};

export default change_link;
