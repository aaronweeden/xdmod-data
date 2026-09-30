MISSING_XDMOD_HOST = (
    "`xdmod_host` parameter or `XDMOD_HOST` environment variable must be set."
)

OUTSIDE_RUNTIME_CONTEXT = (
    "Method is being called outside of the runtime context. Make sure this"
    " method is only called within the body of a `with` statement."
)


def VALUE_NOT_FOUND(name, value, realm=None, valid_values=None):
    value_text = "Raw field" if name == "field" else f"Value for `{name}`"
    realm_text = "" if realm is None else f" in the '{realm}' realm"
    valid_values_sentence = ""
    if valid_values is not None:
        valid_values_str = "', '".join(valid_values)
        valid_values_sentence = f" Value values are: '{valid_values_str}'"
    return f"{value_text} not found{realm_text}: '{value}'.{valid_values_sentence}"


RAW_FIELDS_TYPE_ERROR = "`fields` must be a sequence of strings."

HTTP_401 = "Make sure XDMOD_API_TOKEN is set to a valid API token."

JUPYTERHUB = (
    "If running in an XDMoD-hosted JupyterHub, this is likely a server error"
    " from the JupyterHub. If not running in an XDMoD-hosted JupyterHub, make"
    " sure the `XDMOD_API_TOKEN` environment variable is set before the"
    " `DataWarehouse` is constructed; it should be set to a valid API token"
    " obtained from the XDMoD portal."
)

INVALID_DURATION = "`duration` must be a string or an object with 2 items."

INVALID_FILTERS = (
    "`filters` must be a mapping whose keys are strings and whose values are"
    " strings or sequences of strings."
)

INVALID_RAW_FIELDS = "`fields` must be a sequence of strings."


def GET_RESOURCES(host):
    return (
        f"The requested XDMoD portal ({host}) is not running a version of"
        " XDMoD that supports the `get_resources` method."
    )
