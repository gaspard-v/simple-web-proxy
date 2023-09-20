const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type !== "childList") return;
        mutation.addedNodes.forEach((addedNode) => {
            if (typeof addedNode.hasAttribute !== "function") return;
            if (
                !addedNode.hasAttribute("src") &&
                !addedNode.hasAttribute("href")
            )
                return;
        });
    });
});
