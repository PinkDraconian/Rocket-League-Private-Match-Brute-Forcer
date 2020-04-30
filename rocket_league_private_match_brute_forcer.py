import json

from steam import SteamClient


RLAppId = 252950  # https://steamdb.info/app/252950/
RLEndpoint = 'https://psyonix-rl.appspot.com/Services'
RLKey = 'c338bd36fb8c42b1a431d30add939fc7'
RLUserAgent = 'RL Win/191113.75055.254904 gzip'
RLLanguage = 'INT'
RLFeatureSet = 'PrimeUpdate31'
RLBuildId = '-1878310188'
RLEnvironment = 'Prod'


def steam_login(username, password):
    steam_client = SteamClient()
    two_factor_code = input('Enter 2FA> ')
    steam_client.login(username, password, two_factor_code=two_factor_code)
    return steam_client


def auth():
    pass


def main():
    with open('steam_login.config') as steam_login_config_file:
        steam_login_config = json.load(steam_login_config_file)

    steam_client = steam_login(steam_login_config['username'], steam_login_config['password'])
    steam_id_64 = steam_client.user.steam_id.as_64
    steam_app_ticket = steam_client.get_app_ticket(RLAppId).ticket
    steam_display_name = steam_client.user.name


if __name__ == '__main__':
    main()
