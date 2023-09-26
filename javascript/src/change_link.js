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
        const params = url.searchParams;
        if (url.protocol === "data:") return link;
        if (url.hostname.endsWith(process.env.WEB_PROXY_NETLOC)) {
            const protocol = get_parameter_by_name("web_proxy_method");
            if (protocol && !params.get("web_proxy_method"))
                params.append("web_proxy_method", protocol);
            const port = get_parameter_by_name("web_proxy_port");
            if (port && !params.get("web_proxy_port"))
                params.append("web_proxy_port", protocol);
            return url.href;
        }
        const protocol = url.protocol.slice(0, -1);
        if (!params.get("web_proxy_method")) {
            if (protocol) params.append("web_proxy_method", protocol);
            else {
                const protocol = get_parameter_by_name("web_proxy_method");
                if (protocol) params.append("web_proxy_method", protocol);
            }
        }
        if (!params.get("web_proxy_port")) {
            const port = url.port;
            if (port) params.append("web_proxy_port", url.port);
            else {
                const port = get_parameter_by_name("web_proxy_port");
                if (port) params.append("web_proxy_port", protocol);
            }
        }
        url.search = params;
        url.host = `${url.hostname}.${process.env.WEB_PROXY_NETLOC}`;
        if (process.env.WEB_PROXY_PORT) url.host += `:${base_url.port}`;
        url.protocol = base_url.protocol;
        return url.href;
    } catch (error) {
        return link;
    }
};

export default change_link;
