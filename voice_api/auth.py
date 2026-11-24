import hmac
import logging
import os

from .errors import ApiError

log = logging.getLogger("voice_api")


def _configured_keys():
    raw = os.environ.get("API_KEYS", "")
    return [k.strip() for k in raw.split(",") if k.strip()]


def check_api_key(header_value):
    keys = _configured_keys()
    if not keys:
        log.error("API_KEYS is not set; refusing all requests")
        raise ApiError(500, "server_misconfigured", "The server has no API keys configured.")

    if not header_value:
        raise ApiError(401, "missing_api_key", "Send your key as 'Authorization: Bearer <key>'.")

    scheme, _, token = header_value.partition(" ")
    token = token.strip()
    if scheme.lower() != "bearer" or not token:
        raise ApiError(401, "invalid_auth_header", "Use the format 'Authorization: Bearer <key>'.")

    candidate = token.encode()
    matched = False
    for key in keys:
        matched |= hmac.compare_digest(candidate, key.encode())
    if not matched:
        raise ApiError(401, "invalid_api_key", "That API key is not valid.")