
var observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
        if (mutation.type === "childList") {
            mutation.addedNodes.forEach(function (addedNode) {
                if (typeof addedNode.hasAttribute !== "function")
                    return
                if (addedNode.hasAttribute("src") || addedNode.hasAttribute("href")) {
                    var link = ""
                    if (addedNode.hasAttribute("src"))
                        link = addedNode.getAttribute("src")
                    else if (addedNode.hasAttribute("href"))
                        link = addedNode.getAttribute("href")
                    console.log(`Element avec src ou href trouve : ${link}`);
                    console.log(addedNode);
                }
            });
        }
    });
});

var config = { childList: true, subtree: true };

observer.observe(document, config);
