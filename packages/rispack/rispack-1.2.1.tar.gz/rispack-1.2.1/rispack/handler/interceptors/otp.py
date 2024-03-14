import os
from http import HTTPStatus

import requests

from rispack.aws import get_signed_auth
from rispack.errors import RispackError
from rispack.handler import Request, Response
from rispack.handler.interceptors import BaseInterceptor
from rispack.logger import logger


class InvalidOtpEndpoint(RispackError):
    pass


class OtpInterceptor(BaseInterceptor):
    SETTINGS = {
        "param_name": "otp",
        "header": "X-Authorization-Otp",
        "deprecated": True,
    }

    @classmethod
    def get_param_name(cls):
        return "otp"

    def __init__(self, validate_pin):
        self.validate_pin = validate_pin
        self.endpoint = os.environ.get("OTP_AUTHORIZATION_URL")

        if not self.endpoint:
            raise InvalidOtpEndpoint

    def __call__(self, request: Request):
        id = request.authorizer.get("profile_id")
        otp = self._find_header(request.headers)

        if not otp:
            return Response.forbidden(f"Invalid {self.SETTINGS['header']} header")

        payload = {"otp": otp, "profile_id": id}

        response = requests.post(self.endpoint, auth=get_signed_auth(), json=payload)

        logger.mask_info(
            {
                "endpoint": self.endpoint,
                "message": "debug otp interceptor",
                "payload": payload,
                "response": response,
            }
        )

        if response.status_code != HTTPStatus.OK:
            return Response.forbidden("Invalid OTP")

        return None

    def _find_header(self, headers):
        for header, value in headers.items():
            if header.lower() == self.SETTINGS["header"].lower():
                return value
