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

// fix infinite loop
const mutationAttribute = (mutation) => {
    console.log(mutation);
    const target = mutation.target;
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
        if (mutation.type === "childList") mutationChild(mutation);
        else if (mutation.type === "attributes") mutationAttribute(mutation);
    });
});

export default observer;
