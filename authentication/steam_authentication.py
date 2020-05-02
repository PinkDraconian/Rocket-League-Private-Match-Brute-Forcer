# from steam import SteamClient
from steam.client import SteamClient

from authentication.steam_login_exception import SteamLoginException


def steam_login(username, password, two_factor_code):
    """Logs in to steam
    :param username: username of account
    :type username :class:`str`
    :param password: password of account
    :type password :class:`str`
    :param two_factor_code: valid 2FA code
    :type two_factor_code :class:`str`
    :return steam_client of logged in user
    :rtype `SteamClient`
    """
    steam_client = SteamClient()
    steam_client.login(username, password, two_factor_code=two_factor_code)
    if not steam_client.logged_on:  # Login failed
        raise SteamLoginException('Login failed.')
    return steam_client


def encode_steam_encrypted_app_ticket(steam_encrypted_app_ticket):
    result = [8, steam_encrypted_app_ticket.ticket_version_no, 16]

    crc = steam_encrypted_app_ticket.crc_encryptedticket
    while crc > 127:
        result.append(crc & 127 | 128)
        crc = (crc % 0x100000000) >> 7  # >>> in JavaScript
    result.append(crc)

    result.append(24)
    result.append(steam_encrypted_app_ticket.cb_encrypteduserdata)

    result.append(32)
    result.append(steam_encrypted_app_ticket.cb_encrypted_appownershipticket)

    result.append(42)
    result.append(128)
    result.append(1)
    result.extend(steam_encrypted_app_ticket.encrypted_ticket)

    return ''.join([hex(i)[2:].rjust(2, '0') for i in result]).upper()