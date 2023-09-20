import observer from "./detect_changes";

observer.observe(document, {
    childList: true,
    subtree: true,
    attributes: true,
});
