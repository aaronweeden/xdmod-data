MISSING_XDMOD_HOST = (
    "`xdmod_host` parameter or `XDMOD_HOST` environment variable must be set."
)

HTTP_401 = "Make sure XDMOD_API_TOKEN is set to a valid API token."

JUPYTERHUB = (
    "If running in an XDMoD-hosted JupyterHub, this is likely a server error"
    " from the JupyterHub. If not running in an XDMoD-hosted JupyterHub, make"
    " sure the `XDMOD_API_TOKEN` environment variable is set before the"
    " `DataWarehouse` is constructed; it should be set to a valid API token"
    " obtained from the XDMoD portal."
)

RAW_DATA_COLLECTION_CLOSED = (
    "Connection closed before all data were received! You may need to break"
    " your request into smaller chunks by running `get_raw_data()` multiple"
    " times with fewer days specified for `duration` and then piecing the"
    " resulting data frames back together."
)


def GET_RESOURCES(host):
    return (
        f"The requested XDMoD portal ({host}) is not running a version of"
        " XDMoD that supports the `get_resources` method."
    )
