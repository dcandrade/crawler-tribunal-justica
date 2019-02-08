from selenium import webdriver
import config
from utils.proxies import get_random_proxy


def get_webdriver(silent):
    """
    Starts and configutes a Selenium Chrome Webdriver following the config instructions
    :param silent: If True, the webdriver will run on headless mode
    :return: The configured webdriver instance
    """
    chrome_options = webdriver.ChromeOptions()

    if config.USE_PROXY:
        proxy = get_random_proxy()
        proxy_ip = proxy['ip']
        proxy_port = proxy['port']

        chrome_options.add_argument('--proxy-server=http://{}:{}'.format(proxy_ip, proxy_port))

    if silent:
        prefs = {'profile.managed_default_content_settings.images': 2}  # no imgs
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

    if config.TEST:
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome("/usr/bin/chromedriver", options=chrome_options)

    return driver
