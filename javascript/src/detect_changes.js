import change_link from "./change_link";
const mutationChild = (mutation) => {
    mutation.addedNodes.forEach((addedNode) => {
        if (typeof addedNode.hasAttribute !== "function") return;
        if (!addedNode.hasAttribute("src") && !addedNode.hasAttribute("href"))
            return;
        if (addedNode.hasAttribute("src")) addedNode.src = "/lol";
        if (addedNode.hasAttribute("href")) addedNode.href = "/lol";
        console.log(addedNode);
    });
};

// TODO: fix infinite loop
const mutationAttributes = (mutation) => {
    const target = mutation.target;
    if (!target.href && !target.src) return;
    console.log(change_link("https://www.google.com"));
    return;
    if (mutation.attributeName === "src") {
        target.src = "/lol";
        console.log(target);
    }
    if (mutation.attributeName === "href") {
        target.href = "/lol";
        console.log(target);
    }
};

const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        switch (mutation.type) {
            case "childList":
                return mutationChild(mutation);
            case "attributes":
                return mutationAttributes(mutation);
        }
    });
});

export default observer;
