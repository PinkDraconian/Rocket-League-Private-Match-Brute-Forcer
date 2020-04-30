import gevent.monkey
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()

from steam import SteamClient


RLAppId = 252950  # https://steamdb.info/app/252950/
RLEndpoint = 'https://psyonix-rl.appspot.com/Services'
RLKey = 'c338bd36fb8c42b1a431d30add939fc7'
RLUserAgent = 'RL Win/191113.75055.254904 gzip'
RLLanguage = 'INT'
RLFeatureSet = 'PrimeUpdate31'
RLBuildId = '-1878310188'
RLEnvironment = 'Prod'


def auth():
    pass


def main():

    steam_client = SteamClient()
    two_factor_code = input('Enter 2FA> ')
    steam_client.login('chiliepeppers', 'suchsecure', two_factor_code=two_factor_code)
    print(steam_client.friends)


if __name__ == '__main__':
    main()
