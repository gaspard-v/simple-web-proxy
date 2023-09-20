const change_link = (link) => {
    try {
        const url = new URL(link);
        const base_url = new URL(window.location.href);
        const origin = url.origin;
        const params = url.searchParams;
        params.append("web_proxy_requested_website", origin);
        url.host = base_url.host;
        url.protocol = base_url.protocol;
        url.search = params;
        return url.toString();
    } catch (error) {
        console.error(error);
    }
};

export default change_link;
