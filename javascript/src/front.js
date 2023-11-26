"use strict";
import { encode } from "@abcnews/base-36-text";

const urlForm = document.getElementById("url-form");
urlForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const urlInput = document.getElementById("url-input");
    const urlValue = urlInput.value;
    const urlObj = new URL(urlValue);
    const currentUrl = new URL(window.location.href);
    const urlObjBas32Hostname = encode(urlObj.hostname);
    const newHost = `${urlObjBas32Hostname}.${currentUrl.host}`;
    urlObj.searchParams.append(
        "web_proxy_method",
        urlObj.protocol.slice(0, -1),
    );
    const port = urlObj.port;
    if (port) urlObj.searchParams.append("web_proxy_port", port);
    urlObj.host = newHost;
    urlObj.protocol = currentUrl.protocol;
    window.location.href = urlObj.href;
});
