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
        const param_protocol = get_parameter_by_name("web_proxy_method");
        const param_port = get_parameter_by_name("web_proxy_port");
        if (url.hostname.endsWith(process.env.WEB_PROXY_NETLOC)) {
            const add_method =
                param_protocol && !params.get("web_proxy_method");
            const add_port = param_port && !params.get("web_proxy_port");
            if (add_method) params.append("web_proxy_method", param_protocol);
            if (add_port) params.append("web_proxy_port", param_port);
            return url.href;
        }
        const url_protocol = url.protocol.slice(0, -1);
        if (!params.get("web_proxy_method")) {
            const protocol = url_protocol ? url_protocol : param_protocol;
            if (protocol) params.append("web_proxy_method", protocol);
        }
        const url_port = url.port;
        if (!params.get("web_proxy_port")) {
            const port = url_port ? url_protocol : param_port;
            if (port) params.append("web_proxy_port", port);
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
