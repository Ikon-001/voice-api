from flask import g, jsonify


class ApiError(Exception):
    def __init__(self, status, code, message):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


def error_response(status, code, message):
    body = {
        "error": {
            "code": code,
            "message": message,
            "request_id": g.get("request_id"),
        }
    }
    return jsonify(body), status
