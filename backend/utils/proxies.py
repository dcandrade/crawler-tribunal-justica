import urllib.request
import json
import config
from random import choice


def get_random_proxy():
    """
    Selects a proxy provider from config.PROXY_SERVICES and asks for a new proxy
    :return: A dict containing the proxy data
    """
    service_url = choice(config.PROXY_SERVICES)
    contents = urllib.request.urlopen(service_url).read()

    return json.loads(contents)
