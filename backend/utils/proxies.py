import urllib.request
import json
import config
from random import choice

def get_random_proxy():
    service_url = choice(config.PROXY_SERVICES)
    contents = urllib.request.urlopen(service_url).read()

    return json.loads(contents)
