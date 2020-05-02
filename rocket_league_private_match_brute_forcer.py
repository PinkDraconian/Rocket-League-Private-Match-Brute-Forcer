# This has to be imported before requests module to prevent warning
#   MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors,
#   including RecursionError on Python 3.6. It may also silently lead to incorrect behaviour on Python 3.7.
#   Please monkey-patch earlier. See https://github.com/gevent/gevent/issues/1016
from authentication.steam_authentication import steam_login, encode_steam_encrypted_app_ticket
from authentication.rocket_league_authentication import rl_auth
from rocket_league.requests import get_products_get_player_products_request
import rocket_league_constants
import getpass
import json
import logging
import websocket
import _thread as thread
import time


def rocket_league_connect_to_websocket(url, psy_token, session_id, steam_id_64):
    def on_message(_, message):
        start = message.index('\r\n\r\n')
        start += 4
        message_length = len(message) - start
        if message_length == 0:
            print('[ROCKET LEAGUE] Message received with length 0')
        else:
            message = message[start:]
            message_pretty = json.dumps(json.loads(message))
            print('[ROCKET LEAGUE] Message received:\n{}'.format(message_pretty))

    def on_error(_, error):
        print(error)

    def on_close(_):
        print("[ROCKET LEAGUE] Websocket closed!")

    def on_open(_):
        print('[ROCKET LEAGUE] Connected to websocket!')

        def run(*_):
            ws.send(get_products_get_player_products_request(steam_id_64))
            rocket_league_constants.increase_id()
            time.sleep(1)
            ws.close()
            print("[ROCKET LEAGUE] Closing websocket...")

        thread.start_new_thread(run, ())

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                header={
                                    'PsyToken': psy_token,
                                    'PsySessionID': session_id,
                                    'PsyBuildID': rocket_league_constants.RLBuildId,
                                    'PsyEnvironment': rocket_league_constants.RLEnvironment,
                                    'User-Agent': rocket_league_constants.RLUserAgent
                                },
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    logging.getLogger('websocket').setLevel(logging.INFO)
    ws.run_forever()


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
    steam_encrypted_app_ticket = \
        steam_client.get_encrypted_app_ticket(rocket_league_constants.RLAppId, b'').encrypted_app_ticket
    steam_encoded_encrypted_app_ticket = encode_steam_encrypted_app_ticket(steam_encrypted_app_ticket)
    steam_display_name = steam_client.user.name

    print('[ROCKET LEAGUE] Authenticating with RL servers...')
    rl_auth_response = rl_auth(steam_id_64, steam_encoded_encrypted_app_ticket, steam_display_name)
    if rl_auth_response.get('Error', None) is not None:
        print('[ERROR][ROCKET LEAGUE] Failed to authenticate with the RL servers. Exiting.')
        exit(1)
    print('[ROCKET LEAGUE] Successfully authenticated with the RL servers!')

    print('[ROCKET LEAGUE] Grabbing per_con_url, psy_token and session_id...')
    per_con_url = rl_auth_response['Responses'][0]['Result']['PerConURL']
    psy_token = rl_auth_response['Responses'][0]['Result']['PsyToken']
    session_id = rl_auth_response['Responses'][0]['Result']['SessionID']

    print('[ROCKET LEAGUE] Connecting to websocket...')
    rocket_league_connect_to_websocket(per_con_url, psy_token, session_id, steam_id_64)


if __name__ == '__main__':
    main()
