import change_link from "./change_link";
const mutationChild = (mutation) => {
    mutation.addedNodes.forEach((addedNode) => {
        if (typeof addedNode.hasAttribute !== "function") return;
        if (addedNode.hasAttribute("src") && addedNode.src) {
            if (addedNode.src != change_link(addedNode.src))
                addedNode.src = change_link(addedNode.src);
        } else if (addedNode.hasAttribute("href") && addedNode.href) {
            if (addedNode.href != change_link(addedNode.href))
                addedNode.href = change_link(addedNode.href);
        }
    });
};

const mutationAttributes = (mutation) => {
    const target = mutation.target;
    if (target.href != change_link(target.href)) {
        target.href = change_link(target.href);
    } else if (target.src) {
        if (target.src != change_link(target.src))
            target.src = change_link(target.src);
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
