import os
import re

from fastapi import HTTPException, Request, status

API_TOKEN = "dummy"
OFFLINE = os.environ.get("OFFLINE", "false").lower() == "true"
TOKEN_REGEX = "^(.*) (.*)$"


def _is_valid(authorization_header: str) -> bool:
    if authorization_header and re.fullmatch(TOKEN_REGEX, authorization_header):
        match = re.search(TOKEN_REGEX, authorization_header)
        token_type, token = match.group(1), match.group(2)

        if token_type.lower() == "token" and token == API_TOKEN:
            return True

    return False


def verify_api_token(request: Request):
    if OFFLINE is False and _is_valid(request.headers.get("authorization")) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization"
        )
