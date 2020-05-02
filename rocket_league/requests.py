import json
from rocket_league import rocket_league_constants
from rocket_league.rocket_league_crypto import get_signature


def get_products_get_player_products_request(steam_id_64):
    message_body = json.dumps([{
        'Service': 'Products/GetPlayerProducts',
        'Version': 1,
        'ID': rocket_league_constants.service_id_counter,
        'Params': {
            'PlayerID': 'Steam|{}|0'.format(steam_id_64)
        }
    }])
    signature = get_signature(message_body)
    message_headers = 'PsySig: {}\r\nPsyRequestID: PsyNetMessage_X_{}\r\n\r\n'\
        .format(signature, rocket_league_constants.request_id_counter)
    return message_headers + message_body


def get_game_server_find_private_game_server_request(server_name, password):
    message_body = json.dumps([{
        'Service': 'GameServer/FindPrivateServer',
        'Version': 1,
        'ID': rocket_league_constants.service_id_counter,
        'Params': {
            'ServerName': server_name,
            'Password': password
        }
    }])
    signature = get_signature(message_body)
    message_headers = 'PsySig: {}\r\nPsyRequestID: PsyNetMessage_X_{}\r\n\r\n' \
        .format(signature, rocket_league_constants.request_id_counter)
    return message_headers + message_body
