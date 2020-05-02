# This has to be imported before requests module to prevent warning
#   MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors,
#   including RecursionError on Python 3.6. It may also silently lead to incorrect behaviour on Python 3.7.
#   Please monkey-patch earlier. See https://github.com/gevent/gevent/issues/1016
from authentication.steam_authentication import steam_login, encode_steam_encrypted_app_ticket

import base64
import hashlib
import getpass
import hmac
import json
import requests

RLAppId = 252950  # https://steamdb.info/app/252950/
RLEndpoint = 'https://psyonix-rl.appspot.com/Services'
RLKey = 'c338bd36fb8c42b1a431d30add939fc7'
RLUserAgent = 'RL Win/191113.75055.254903 gzip'
RLLanguage = 'INT'
RLFeatureSet = 'PrimeUpdate31'  # Edit after Rocket League by launching the game with the `-log` option and looking for the new value
RLBuildId = '-1878310188'  # Edit after Rocket League by launching the game with the `-log` option and looking for the new value
RLEnvironment = 'Prod'


def rl_auth(steam_id_64, steam_encoded_encrypted_app_ticket, steam_display_name):
    data = json.dumps([{
        'Service': 'Auth/AuthPlayer',
        'Version': 1,
        'ID': 1,
        'Params': {
            'Platform': 'Steam',
            'PlayerName': steam_display_name,
            'PlayerID': str(steam_id_64),
            'Language': RLLanguage,
            'AuthTicket': steam_encoded_encrypted_app_ticket,
            'BuildRegion': '',
            'FeatureSet': RLFeatureSet,
            'bSkipAuth': False
        }
    }], separators=(',', ':'))

    digest = hmac.new(RLKey.encode(), msg=('-' + data).encode(), digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': RLUserAgent,
        'Cache-Control': 'no-cache',
        'PsyBuildID': RLBuildId,
        'PsyEnvironment': RLEnvironment,
        'PsyRequestID': 'PsyNetMessage_X_0',
        'PsySig': signature
    }

    r = requests.post(url=RLEndpoint, headers=headers, data=data)
    return json.loads(r.text)


def main():
    print('[STEAM] Parsing config file...')
    with open('steam_login.config') as steam_login_config_file:
        steam_login_config = json.load(steam_login_config_file)

    print('[STEAM] Logging in...')
    two_factor_code = getpass.getpass('Enter 2FA> ')
    steam_client = steam_login(steam_login_config['username'], steam_login_config['password'], two_factor_code)
    print('[STEAM] Successfully logged in!')

    print('[STEAM] Getting id_64, encrypted_app_ticket and display_name...')
    steam_id_64 = steam_client.user.steam_id.as_64
    steam_encrypted_app_ticket = steam_client.get_encrypted_app_ticket(252950, b'').encrypted_app_ticket
    steam_encoded_encrypted_app_ticket = encode_steam_encrypted_app_ticket(steam_encrypted_app_ticket)

    steam_display_name = steam_client.user.name
    print('[ROCKET LEAGUE] Authenticating with RL servers...')
    rl_auth_response = rl_auth(steam_id_64, steam_encoded_encrypted_app_ticket, steam_display_name)
    if rl_auth_response.get('Error', None) is not None:
        print('[ERROR][ROCKET LEAGUE] Failed to authenticate with the RL servers. Exiting.')
        exit(1)
    print('[ROCKET LEAGUE] Successfully authenticated with the RL servers')


if __name__ == '__main__':
    main()
