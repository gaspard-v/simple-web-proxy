import get_cookie from "./get_cookie";
import get_parameter_by_name from "./get_parameter";

const get_requested_website = () => {
    let requested_website = get_cookie("web_proxy_requested_website");
    if (!requested_website)
        requested_website = get_parameter_by_name(
            "web_proxy_requested_website",
        );
    if (!requested_website) throw new Error("No web_proxy_requested_website");
    return requested_website;
};

export default get_requested_website;
