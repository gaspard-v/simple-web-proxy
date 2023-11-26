"use strict";
import observer from "./detect_changes";
import patch_cookies from "./patch_cookies";
import inject from "./inject_fetch";
observer.observe(document, {
    childList: true,
    subtree: true,
    attributes: true,
});

patch_cookies();
inject();
