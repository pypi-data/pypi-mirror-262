"""Authorization implementations for requests to a 10Duke API.

These classes are used as hooks for the requests. Request object to add Authorization headers to
outgoing HTTP requests.
"""
from typing import Callable

from requests import PreparedRequest
from requests.auth import AuthBase

from ..exceptions.validation import InvalidArgumentError


class IdTokenAuth(AuthBase):
    """ID Token Auth hook - used with Open ID Connect in public applications."""

    def __init__(self, id_token_callable: Callable[[], str]) -> None:
        """Construct an IdTokenAuth provider (hook).

        Args:
            id_token_callable: A callable that returns the latest id_token.
        """
        if id_token_callable is None:
            raise InvalidArgumentError("id_token_callable")
        self.id_token_callable = id_token_callable

    def __call__(self, r: PreparedRequest):
        """Mutate outgoing request (adding authorization header).

        Args:
            r: Outgoing request.
        """
        r.headers["Authorization"] = f"IdToken {self.id_token_callable()}"
        return r

    def __eq__(self, other):
        """Return True if instances are equal; otherwise False.

        Equality is tested by retrieving the id_token for each instance and comparing them.
        """
        return (
            self.id_token_callable()
            == getattr(other, "id_token_callable", lambda: None)()
        )

    def __ne__(self, other):
        """Return True if instances are not equal; otherwise False.

        Equality is tested by retrieving the id_token for each instance and comparing them.
        """
        return not self == other
