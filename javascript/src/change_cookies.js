const get_parameter_by_name = (name) => {
    name = name.replace(/[\[\]]/g, "\\$&");
    const regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)");
    const results = regex.exec(window.location.href);
    if (!results) return null;
    if (!results[2]) return "";
    return decodeURIComponent(results[2].replace(/\+/g, " "));
};

const change_cookies = () => {
    const parameter = get_parameter_by_name("web_proxy_requested_website");
    if (parameter)
        document.cookie = `web_proxy_requested_website=${parameter}; path=/`;
};
export default change_cookies;
