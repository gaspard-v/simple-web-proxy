import get_parameter_by_name from "./get_parameter";

const check_domain = (full_domaine, partial_domain) =>
    full_domaine.toLowerCase().endsWith(partial_domain.toLowerCase());

const remove_domain_prefix = () => {
    const cookies = document.cookie.split("; ");
    window.activeCookies = [];
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const cookieParts = cookie.split("=");
        if (cookieParts.length !== 2) continue;
        const cookie_name = cookieParts[0];
        const cookie_value = cookieParts[1];
        const parties = cookie_name.split(/_(.+)/);
        if (parties.length !== 3) continue;
        const prefix = parties[0];
        const cookie_real_name = parties[1];
        const base_url = new URL(window.location.href);
        const host = base_url.host;
        if (!check_domain(host, prefix)) continue;
        document.cookie = `${cookie_name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; Secure; SameSite=None`; // delete cookie
        document.cookie = `${cookie_real_name}=${cookie_value}; path=/; Secure; SameSite=None`;
        window.activeCookies.push([
            cookie_real_name,
            cookie_name,
            cookie_value,
        ]);
    }
};

const add_domain_prefix = () => {
    window.addEventListener("beforeunload", (e) => {
        if (!window.activeCookies) return;
        window.activeCookies.forEach(
            ([cookie_real_name, cookie_name, cookie_value]) => {
                document.cookie = `${cookie_real_name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; Secure; SameSite=None`; // delete cookie
                document.cookie = `${cookie_name}=${cookie_value}; path=/; Secure; SameSite=None`;
            },
        );
    });
};

const change_cookies = () => {
    remove_domain_prefix();
    add_domain_prefix();
    const parameter = get_parameter_by_name("web_proxy_requested_website");
    if (parameter)
        document.cookie = `web_proxy_requested_website=${parameter}; path=/`;
};
export default change_cookies;
