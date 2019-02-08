POOL_SIZE = 1               # Size of the crawler pool for each court (See crawler.async_pool.CrawlerPool)
USE_PROXY = False           # Use or not proxies to hide the origin of the requests
TEST = False                # If running locally (not in Docker), set this to True
DB_NAME = 'process-crawler' # DB name in Mongo


COURTS = {                  # Accepted courts. More courts can be added if they follow tha same website patterns
    'TJSP': {
        'name': 'Tribunal de São Paulo',
        'url': 'https://esaj.tjsp.jus.br/cpopg/open.do',
        'delimiter': '8.26'
    },
    'TJMS': {
        'name': 'Tribunal do Mato Grosso do Sul',
        'url': 'https://esaj.tjms.jus.br/cpopg5/open.do',
        'delimiter': '8.12'
    }
}

PROXY_SERVICES = ['https://api.getproxylist.com/proxy', "https://gimmeproxy.com/api/getProxy"] # Proxy list servers