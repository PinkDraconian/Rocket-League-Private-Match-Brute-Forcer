RLAppId = 252950  # https://steamdb.info/app/252950/
RLEndpoint = 'https://psyonix-rl.appspot.com/Services'
RLKey = 'c338bd36fb8c42b1a431d30add939fc7'
RLUserAgent = 'RL Win/191113.75055.254903 gzip'
RLLanguage = 'INT'
# Edit after Rocket League by launching the game with the `-log` option and looking for the new value
RLFeatureSet = 'PrimeUpdate31'
# Edit after Rocket League by launching the game with the `-log` option and looking for the new value
RLBuildId = '-1878310188'
RLEnvironment = 'Prod'


def increase_id():
    global request_id_counter
    request_id_counter += 1
    global service_id_counter
    service_id_counter += 1


# Increase after each request
request_id_counter = 0
# Increase after each service
service_id_counter = 1
