import selenium
from selenium import webdriver
import config
from utils.proxies import get_random_proxy

def get_webdriver(silent):
    chromeOptions = webdriver.ChromeOptions()

    if config.USE_PROXY:
        proxy = get_random_proxy()
        proxy_ip = proxy['ip']
        proxy_port = proxy['port']

        chromeOptions.add_argument('--proxy-server=http://{}:{}'.format(proxy_ip, proxy_port))

    if silent:
        prefs = {'profile.managed_default_content_settings.images': 2}  # no imgs
        chromeOptions.add_experimental_option("prefs", prefs)
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-dev-shm-usage')
    
    if config.TEST:
        driver = webdriver.Chrome(options=chromeOptions)
    else:
        driver = webdriver.Chrome("/usr/bin/chromedriver", options=chromeOptions)

    return driver