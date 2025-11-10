import asyncio
from playwright.async_api import async_playwright

async def analisar_logo():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(60000)  # 60 segundos
        
        url = 'https://www.comprasparaguai.com.br/fone-de-ouvido-xiaomi-mi-redmi-buds-6-active-m2344e1-rosa__4393157/'
        print(f'🔍 Acessando: {url}\n')
        
        await page.goto(url, wait_until='domcontentloaded')
        await asyncio.sleep(3)  # Esperar carregar
        
        print('=' * 80)
        print('PROCURANDO LOGO DA LOJA NA PÁGINA DE DETALHES')
        print('=' * 80)
        
        # 1. Procurar por seletores comuns de logo
        selectors = [
            ('Logo vendedor', 'img[alt*="vendedor" i]'),
            ('Logo seller', '.seller-logo img, .store-logo img'),
            ('Logo loja', 'img[alt*="loja" i]'),
            ('Link loja com img', 'a[href*="loja"] img'),
            ('Imagens com logo', 'img[src*="logo" i]'),
            ('Header seller', '.header-seller img, .seller-info img'),
        ]
        
        for nome, seletor in selectors:
            elements = await page.query_selector_all(seletor)
            if elements:
                print(f'\n✅ {nome} ({seletor}):')
                for elem in elements[:5]:  # Limitar a 5
                    src = await elem.get_attribute('src')
                    alt = await elem.get_attribute('alt') or ''
                    print(f'   - src: {src}')
                    print(f'     alt: {alt}')
        
        # 2. Listar todas as imagens da página
        print('\n' + '=' * 80)
        print('TODAS AS IMAGENS DA PÁGINA (primeiras 20):')
        print('=' * 80)
        
        all_images = await page.query_selector_all('img')
        for i, img in enumerate(all_images[:20]):
            src = await img.get_attribute('src')
            alt = await img.get_attribute('alt') or '(sem alt)'
            print(f'{i+1}. {alt[:60]}: {src[:80] if src else "sem src"}')
        
        # 3. Procurar por informações do vendedor
        print('\n' + '=' * 80)
        print('INFORMAÇÕES DO VENDEDOR:')
        print('=' * 80)
        
        # Procurar texto que mencione vendedor/loja
        seller_texts = await page.query_selector_all('*:has-text("Vendido por"), *:has-text("Loja"), *:has-text("Seller")')
        for elem in seller_texts[:10]:
            text = await elem.inner_text()
            print(f'   {text[:100]}')
        
        await browser.close()

asyncio.run(analisar_logo())
