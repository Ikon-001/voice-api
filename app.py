import logging
import uuid

from flask import Flask, Response, g, jsonify, request
from werkzeug.exceptions import HTTPException

from voice_api.audio import to_wav_bytes
from voice_api.engines import get_speech_engine, speech_languages
from voice_api.errors import ApiError, error_response

MAX_TEXT_CHARS = 500
MIN_SPEED, MAX_SPEED = 0.7, 1.2

app = Flask(__name__)
log = logging.getLogger("voice_api")


@app.before_request
def assign_request_id():
    g.request_id = uuid.uuid4().hex[:12]


@app.after_request
def add_request_id_header(response):
    response.headers["X-Request-ID"] = g.get("request_id", "")
    return response


@app.errorhandler(ApiError)
def handle_api_error(err):
    return error_response(err.status, err.code, err.message)


@app.errorhandler(HTTPException)
def handle_http_error(err):
    code = (err.name or "error").lower().replace(" ", "_")
    return error_response(err.code or 500, code, err.description or err.name)


@app.errorhandler(Exception)
def handle_unexpected(err):
    log.exception("unhandled error (request %s)", g.get("request_id"))
    return error_response(500, "internal_error", "Something went wrong on our side.")


@app.get("/")
def status():
    return jsonify({"status": "ok"})


@app.post("/v1/speech")
def speech():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        raise ApiError(400, "invalid_request", "Send a JSON object as the request body.")

    text = body.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ApiError(400, "invalid_request", "'text' is required and must be a non-empty string.")
    text = text.strip()
    if len(text) > MAX_TEXT_CHARS:
        raise ApiError(400, "text_too_long", f"'text' must be at most {MAX_TEXT_CHARS} characters.")

    language = body.get("language", "pcm")
    engine = get_speech_engine(language) if isinstance(language, str) else None
    if engine is None:
        raise ApiError(400, "unsupported_language", f"Supported languages: {', '.join(speech_languages())}.")

    speed = body.get("speed", 1.0)
    if isinstance(speed, bool) or not isinstance(speed, (int, float)) or not MIN_SPEED <= speed <= MAX_SPEED:
        raise ApiError(400, "invalid_request", f"'speed' must be a number from {MIN_SPEED} to {MAX_SPEED}.")

    if body.get("format", "wav") != "wav":
        raise ApiError(400, "unsupported_format", "Only 'wav' is supported at the moment.")

    try:
        samples, rate = engine.synthesize(text, float(speed))
    except Exception:
        log.exception("engine failure (request %s)", g.get("request_id"))
        raise ApiError(500, "engine_error", "The speech engine failed to generate audio.")

    return Response(to_wav_bytes(samples, rate), mimetype="audio/wav")
