MISSING_XDMOD_HOST = (
    "`xdmod_host` parameter or `XDMOD_HOST` environment variable must be set."
)


def VALUE_NOT_FOUND(name, value, realm=None, valid_values=None):
    realm_text = "" if realm is None else f" in the '{realm}' realm"
    valid_values_sentence = ""
    if valid_values is not None:
        valid_values_str = "', '".join(valid_values)
        valid_values_sentence = f" Value values are: '{valid_values_str}'"
    return (
        f"Value for `{name}` not found{realm_text}: '{value}'.{valid_values_sentence}"
    )


HTTP_401 = "Make sure XDMOD_API_TOKEN is set to a valid API token."

JUPYTERHUB = (
    "If running in an XDMoD-hosted JupyterHub, this is likely a server error"
    " from the JupyterHub. If not running in an XDMoD-hosted JupyterHub, make"
    " sure the `XDMOD_API_TOKEN` environment variable is set before the"
    " `DataWarehouse` is constructed; it should be set to a valid API token"
    " obtained from the XDMoD portal."
)


def GET_RESOURCES(host):
    return (
        f"The requested XDMoD portal ({host}) is not running a version of"
        " XDMoD that supports the `get_resources` method."
    )
