import json
from rocket_league_crypto import get_signature


def get_products_get_player_products_request(request_id, service_id, steam_id_64):
    message_body = json.dumps([{
        'Service': 'Products/GetPlayerProducts',
        'Version': 1,
        'ID': service_id,
        'Params': {
            'PlayerID': 'Steam|{}|0'.format(steam_id_64)
        }
    }])
    signature = get_signature(message_body)
    message_headers = 'PsySig: {}\r\nPsyRequestID: PsyNetMessage_X_{}\r\n\r\n'.format(signature, request_id)
    return message_headers + message_body
