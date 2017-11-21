# Copyright (C) 2015 Twitter, Inc.

"""Container for all errors raised by the Twitter Ads SDK."""


class Error(Exception):
    """The base class for all SDK error types."""

    def __init__(self, response, **kwargs):
        self._response = response
        self._code = kwargs.get('code', response.code)

        if response.body and 'errors' in response.body:
            self._details = kwargs.get('details', response.body.get('errors'))
        else:
            self._details = None

    @property
    def response(self):
        return self._response

    @property
    def code(self):
        return self._code

    @property
    def details(self):
        return self._details

    def __repr__(self):
        return '<{name} object at {mem} code={code} details={details}>'.format(
            name=self.__class__.__name__,
            mem=hex(id(self)),
            code=getattr(self, 'code'),
            details=getattr(self, 'details')
        )

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def from_response(response):
        """Returns the correct error type from a ::class::`Response` object."""
        if response.code:
            return ERRORS[response.code](response)
        else:
            return Error(response)


class ClientError(Error):
    """Parent class for preventable client errors."""


class BadRequest(ClientError):
    """Bad Request (400)."""


class NotAuthorized(ClientError):
    """Not Authorized (401)."""


class Forbidden(ClientError):
    """Forbidden (403)."""


class NotFound(ClientError):
    """Forbidden (404)."""


class RateLimit(ClientError):
    """Rate Limit (429)."""

    def __init__(self, response, **kwargs):
        super(RateLimit, self).__init__(response, **kwargs)
        self._retry_after = response.headers.get('retry-after', None)
        self._reset_at = response.headers.get('rate_limit_reset', None)

    @property
    def reset_at(self):
        return self._reset_at

    @property
    def retry_after(self):
        return self._retry_after


class ServerError(Error):
    """Server Error (500)."""


class ServiceUnavailable(ServerError):
    """Service Unavailable (503)."""

    def __init__(self, response, **kwargs):
        super(ServiceUnavailable, self).__init__(response, **kwargs)
        self._retry_after = response.headers.get('retry-after', None)

    @property
    def retry_after(self):
        return self._retry_after


ERRORS = {
    400: BadRequest,
    401: NotAuthorized,
    403: Forbidden,
    404: NotFound,
    429: RateLimit,
    500: ServerError,
    503: ServiceUnavailable
}
