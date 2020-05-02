import json
import requests
import rocket_league_constants
from rocket_league_crypto import get_signature


def rl_auth(steam_id_64, steam_encoded_encrypted_app_ticket, steam_display_name):
    data = json.dumps([{
        'Service': 'Auth/AuthPlayer',
        'Version': 1,
        'ID': rocket_league_constants.service_id_counter,
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

    signature = get_signature(data)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': rocket_league_constants.RLUserAgent,
        'Cache-Control': 'no-cache',
        'PsyBuildID': rocket_league_constants.RLBuildId,
        'PsyEnvironment': rocket_league_constants.RLEnvironment,
        'PsyRequestID': 'PsyNetMessage_X_{}'.format(rocket_league_constants.request_id_counter),
        'PsySig': signature
    }

    rocket_league_constants.increase_id()

    r = requests.post(url=rocket_league_constants.RLEndpoint, headers=headers, data=data)
    return json.loads(r.text)
