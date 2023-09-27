const urlForm = document.getElementById("url-form");
urlForm.addEventListener("submit", function (event) {
  event.preventDefault();
  const urlInput = document.getElementById("url-input");
  const urlValue = urlInput.value;
  const urlObj = new URL(urlValue);
  const currentUrl = new URL(window.location.href);
  const newHost = `${urlObj.hostname}.${currentUrl.host}`;
  urlObj.searchParams.append("web_proxy_method", urlObj.protocol.slice(0, -1));
  const port = urlObj.port;
  if (port) urlObj.searchParams.append("web_proxy_port", port);
  urlObj.host = newHost;
  urlObj.protocol = currentUrl.protocol;
  window.location.href = urlObj.href;
});
