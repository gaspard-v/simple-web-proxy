import observer from "./detect_changes";
import change_cookies from "./change_cookies";

observer.observe(document, {
    childList: true,
    subtree: true,
    attributes: true,
});

change_cookies();
