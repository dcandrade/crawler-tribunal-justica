COURTS = {
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

POOL_SIZE = 5
DB_NAME = 'process-crawler'
USE_PROXY = False
PROXY_SERVICES = ['https://api.getproxylist.com/proxy', "https://gimmeproxy.com/api/getProxy"]
