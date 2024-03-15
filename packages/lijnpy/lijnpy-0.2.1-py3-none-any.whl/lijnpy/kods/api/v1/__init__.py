import os

from lijnpy import _logger
from lijnpy.rest_adapter import RestAdapter

API_KEY = os.environ.get("DELIJN_API_KEY", "NO_API_KEY")
_rest_adapter = RestAdapter(
    "api.delijn.be/DLKernOpenData/api",
    API_KEY,
    "v1",
    True,
    _logger,
)
