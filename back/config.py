# COURTS = [
#     'TJSP',
#     'TJMS'
# ]

# DELIMITERS = {
#         'TJSP' : '8.26',
#         'TJMS' : '8.12'
# }

# BASE_URLS = {
#     'TJSP' : 'https://esaj.tjsp.jus.br/cpopg/open.do',
#     'TJMS' : 'https://esaj.tjms.jus.br/cpopg5/open.do',
# }

COURTS = {
    'TJSP': {
        'name'      : 'Tribunal de São Paulo',
        'url'       : 'https://esaj.tjsp.jus.br/cpopg/open.do',
        'delimiter' : '8.26'
    },
    'TJMS': {
        'name'      : 'Tribunal do Mato Grosso do Sul',
        'url'       : 'https://esaj.tjms.jus.br/cpopg5/open.do',
        'delimiter' : '8.12'
    }
}

POOL_SIZE = 2