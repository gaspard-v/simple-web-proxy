"use strict";
import observer from "./detect_changes";
import patch_cookies from "./patch_cookies";
import inject from "./inject_fetch";
import { test } from "./base36";
observer.observe(document, {
    childList: true,
    subtree: true,
    attributes: true,
});

patch_cookies();
inject();
test();
