import change_link from "./change_link";

const inject_fetch = () => {
    const orignal_fetch = window.fetch;
    window.fetch = (input, init = undefined) => {
        console.log(input);
        if (typeof input == "string") {
            input = change_link(input);
        } else {
            const new_url = change_link(input.url);
            const originalRequest = input;
            input = new Request(new_url, {
                method: originalRequest.method,
                headers: originalRequest.headers,
                body: originalRequest.body,
                mode: originalRequest.mode,
                credentials: originalRequest.credentials,
                cache: originalRequest.cache,
                redirect: originalRequest.redirect,
                referrer: originalRequest.referrer,
                integrity: originalRequest.integrity,
                keepalive: originalRequest.keepalive,
                signal: originalRequest.signal,
            });
        }
        return orignal_fetch.apply(this, [input, init]);
    };
};

const inject_xhr = () => {
    const original_xhr_open = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = (
        method,
        url,
        async = true,
        user = null,
        password = null,
    ) => {
        if (typeof url == "string") {
            url = change_link(url);
        } else {
            url = change_link(url.toString());
        }
        return original_xhr_open.apply(this, [
            method,
            url,
            async,
            user,
            password,
        ]);
    };
};

const inject = () => {
    inject_fetch();
    inject_xhr();
};

export default inject;
