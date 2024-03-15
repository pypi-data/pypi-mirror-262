import os
from http import HTTPStatus

import requests

from rispack.aws import get_signed_auth
from rispack.errors import RispackError
from rispack.handler import Request, Response
from rispack.handler.interceptors import BaseInterceptor


class InvalidPinEndpoint(RispackError):
    pass


class PinInterceptor(BaseInterceptor):
    SETTINGS = {
        "param_name": "pin",
        "header": "X-Authorization-Pin",
        "iam": True,
        "deprecated": True,
    }

    def __init__(self, validate_pin):
        self.validate_pin = validate_pin
        self.endpoint = os.environ.get("PIN_AUTHORIZATION_URL")

        if not self.endpoint:
            raise InvalidPinEndpoint

    def __call__(self, request: Request):
        id = request.authorizer.get("profile_id")
        pin = self._find_header(request.headers)

        if not pin:
            return Response.forbidden(f"Invalid {self.SETTINGS['header']} header")

        payload = {"pin": pin, "profile_id": id}

        response = requests.post(self.endpoint, auth=get_signed_auth(), json=payload)

        if response.status_code != HTTPStatus.OK:
            return Response.forbidden("Invalid PIN")

        return None

    def _find_header(self, headers):
        for header, value in headers.items():
            if header.lower() == self.SETTINGS["header"].lower():
                return value
