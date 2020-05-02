# This has to be imported before requests module to prevent warning
#   MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors,
#   including RecursionError on Python 3.6. It may also silently lead to incorrect behaviour on Python 3.7.
#   Please monkey-patch earlier. See https://github.com/gevent/gevent/issues/1016
from authentication.steam_authentication import steam_login, encode_steam_encrypted_app_ticket
from authentication.rocket_league_authentication import rl_auth
import getpass
import json


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
