import base64
import hashlib
import hmac
import json
import requests
import rocket_league_constants


def rl_auth(steam_id_64, steam_encoded_encrypted_app_ticket, steam_display_name):
    data = json.dumps([{
        'Service': 'Auth/AuthPlayer',
        'Version': 1,
        'ID': 1,
        'Params': {
            'Platform': 'Steam',
            'PlayerName': steam_display_name,
            'PlayerID': str(steam_id_64),
            'Language': rocket_league_constants.RLLanguage,
            'AuthTicket': steam_encoded_encrypted_app_ticket,
            'BuildRegion': '',
            'FeatureSet': rocket_league_constants.RLFeatureSet,
            'bSkipAuth': False
        }
    }], separators=(',', ':'))

    digest = hmac.new(rocket_league_constants.RLKey.encode(),
                      msg=('-' + data).encode(), digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': rocket_league_constants.RLUserAgent,
        'Cache-Control': 'no-cache',
        'PsyBuildID': rocket_league_constants.RLBuildId,
        'PsyEnvironment': rocket_league_constants.RLEnvironment,
        'PsyRequestID': 'PsyNetMessage_X_0',
        'PsySig': signature
    }

    r = requests.post(url=rocket_league_constants.RLEndpoint, headers=headers, data=data)
    return json.loads(r.text)