from functools import wraps
from nacl.signing import VerifyKey
from .enums import InteractionType, InteractionResponseType

def verify_key(raw_body: bytes, signature: str, timestamp: str, client_public_key: str) -> bool:
    message = timestamp.encode() + raw_body
    try:
        vk = VerifyKey(bytes.fromhex(client_public_key))
        vk.verify(message, bytes.fromhex(signature))
        return True
    except Exception as ex:
        print(ex)
    return False


def verify_key_decorator(client_public_key):
    from flask import request, jsonify

    # https://stackoverflow.com/questions/51691730/flask-middleware-for-specific-route
    def _decorator(f):
        @wraps(f)
        def __decorator(*args, **kwargs):
            # Verify request
            signature = request.headers.get('X-Signature-Ed25519')
            timestamp = request.headers.get('X-Signature-Timestamp')
            if signature is None or timestamp is None or not verify_key(request.data, signature, timestamp, client_public_key):
                return 'Bad request signature', 401

            # Automatically respond to pings
            if request.json and request.json.get('type') == InteractionType.PING:
                return jsonify({
                    'type': InteractionResponseType.PONG
                })

            # Pass through
            return f(*args, **kwargs)
        return __decorator
    return _decorator
