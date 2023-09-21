import get_parameter_by_name from "./get_parameter";

const change_cookies = () => {
    const parameter = get_parameter_by_name("web_proxy_requested_website");
    if (parameter)
        document.cookie = `web_proxy_requested_website=${parameter}; path=/`;
};
export default change_cookies;
