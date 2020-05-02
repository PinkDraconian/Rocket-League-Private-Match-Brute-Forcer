import base64
import hashlib
import hmac
import rocket_league_constants


def get_signature(data):
    digest = hmac.new(rocket_league_constants.RLKey.encode(),
                      msg=('-' + data).encode(), digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode()
    return signature
