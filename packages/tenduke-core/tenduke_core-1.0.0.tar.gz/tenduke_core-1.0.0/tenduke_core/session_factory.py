"""Configure requests session for use by a client."""
import functools
from typing import Dict, Optional, Tuple

from requests import Session
from requests.auth import AuthBase


def session_factory(
    auth: Optional[AuthBase] = None,
    timeout: Tuple[float, float] = (30.0, 30.0),
    proxies: Optional[Dict[str, str]] = None,
):
    """Create a requests session configured for the application.

    Args:
        auth: Authorization hook.
        timeout: Connect and read timeout values.
        proxies: Proxy definitions.

    Returns:
        A session configured to use the parameters passed in for all requests made using the
        session.
    """
    session = Session()
    session.request = functools.partial( # type: ignore[method-assign]
        session.request, timeout=timeout, proxies=proxies
    )
    session.auth = auth
    return session
