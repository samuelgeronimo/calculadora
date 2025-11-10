"""
Configuração dos marketplaces para comparação de preços
FOCADO NOS 4 MELHORES MARKETPLACES
"""

MARKETPLACES = {
    'mercadolivre': {
        'nome': 'Mercado Livre',
        'url_base': 'https://www.mercadolivre.com.br',
        'url_busca': 'https://lista.mercadolivre.com.br/{query}',
        'logo': 'https://http2.mlstatic.com/frontend-assets/ml-web-navigation/ui-navigation/5.21.22/mercadolibre/logo__large_plus.png',
        'cor': '#FFE600',
        'seletores': {
            'container': 'ol.ui-search-layout',
            'item': 'li.ui-search-layout__item',
            'titulo': 'a.poly-component__title',
            'preco': 'span.andes-money-amount__fraction',
            'link': 'a.poly-component__title',
            'imagem': 'img.poly-component__picture'
        }
    },
    'shopee': {
        'nome': 'Shopee',
        'url_base': 'https://shopee.com.br',
        'url_busca': 'https://shopee.com.br/search?keyword={query}',
        'logo': 'https://deo.shopeemobile.com/shopee/shopee-pcmall-live-sg/assets/icon_shopee_logo_1.41022f5ab5df8b9ca7e2.svg',
        'cor': '#EE4D2D',
        'seletores': {
            'container': 'div.shop-search-result-view__result',
            'item': 'div.col-xs-2-4',
            'titulo': 'div[data-sqe="name"]',
            'preco': 'span.M84Lxd',
            'link': 'a[data-sqe="link"]',
            'imagem': 'img'
        }
    },
    'casasbahia': {
        'nome': 'Casas Bahia',
        'url_base': 'https://www.casasbahia.com.br',
        'url_busca': 'https://www.casasbahia.com.br/busca/{query}',
        'logo': 'https://www.casasbahia.com.br/assets/images/logo.svg',
        'cor': '#F15A22',
        'seletores': {
            'container': 'div[data-testid="product-list"]',
            'item': 'div[data-testid="product-card"]',
            'titulo': 'h2[data-testid="product-title"]',
            'preco': 'div[data-testid="price-value"]',
            'link': 'a[data-testid="product-card-container"]',
            'imagem': 'img[data-testid="product-image"]'
        }
    },
    'kabum': {
        'nome': 'KaBuM!',
        'url_base': 'https://www.kabum.com.br',
        'url_busca': 'https://www.kabum.com.br/busca/{query}',
        'logo': 'https://static.kabum.com.br/conteudo/icons/logo-kabum.svg',
        'cor': '#FF6500',
        'seletores': {
            'container': 'div#listagem-produtos',
            'item': 'article.productCard',
            'titulo': 'span.nameCard',
            'preco': 'span.priceCard',
            'link': 'a.productLink',
            'imagem': 'img.imageCard'
        }
    }
}


def get_all_marketplaces():
    """Retorna configuração de todos os marketplaces"""
    return MARKETPLACES


def get_marketplace(marketplace_id):
    """Retorna configuração de um marketplace específico"""
    return MARKETPLACES.get(marketplace_id)


def get_marketplace_names():
    """Retorna lista com nomes de todos os marketplaces"""
    return [mp['nome'] for mp in MARKETPLACES.values()]
