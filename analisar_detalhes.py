import asyncio
from playwright.async_api import async_playwright

async def analisar_pagina():
    url = "https://www.comprasparaguai.com.br/console-microsoft-xbox-series-x-1tb-ssd-usa-preto__4455920/"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        print(f"🔍 Acessando: {url}")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(8)
        
        # Scroll completo
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(3)
        
        print("\n" + "="*70)
        print("ANÁLISE DA PÁGINA DE DETALHES")
        print("="*70)
        
        # H1 - Nome
        h1 = await page.query_selector('h1')
        if h1:
            print(f"\n✅ NOME (h1): {await h1.inner_text()}")
        
        # Todas as imagens grandes
        print("\n📸 IMAGENS PRINCIPAIS (>200px):")
        imgs = await page.query_selector_all('img')
        count = 0
        for img in imgs:
            try:
                box = await img.bounding_box()
                if box and (box['width'] > 200 or box['height'] > 200):
                    src = await img.get_attribute('src') or await img.get_attribute('data-src')
                    alt = await img.get_attribute('alt') or ''
                    if src and 'logo' not in src.lower() and 'icon' not in src.lower():
                        print(f"  - {src[:80]}... (alt: {alt[:40]})")
                        count += 1
                        if count >= 3:
                            break
            except:
                pass
        
        # Preço - buscar em múltiplos lugares
        print("\n💰 PREÇOS ENCONTRADOS:")
        precos = await page.query_selector_all('[class*="prec"], [class*="price"], .valor, .value')
        for i, p in enumerate(precos[:5]):
            try:
                texto = await p.inner_text()
                texto = texto.strip()
                if texto and ('$' in texto or 'R$' in texto or 'US$' in texto):
                    print(f"  {i+1}. {texto[:50]}")
            except:
                pass
        
        # Todas as listas (possíveis specs)
        print("\n📋 LISTAS ENCONTRADAS:")
        uls = await page.query_selector_all('ul')
        for i, ul in enumerate(uls[:10]):
            try:
                items = await ul.query_selector_all('li')
                if 2 <= len(items) <= 20:
                    first_item = await items[0].inner_text()
                    first_item = first_item.strip()[:60]
                    if first_item and 'menu' not in first_item.lower():
                        print(f"  Lista {i+1}: {len(items)} itens - Ex: {first_item}")
            except:
                pass
        
        # Tabelas
        print("\n📊 TABELAS:")
        tables = await page.query_selector_all('table')
        for i, table in enumerate(tables[:3]):
            try:
                rows = await table.query_selector_all('tr')
                if rows:
                    first_row = await rows[0].inner_text()
                    print(f"  Tabela {i+1}: {len(rows)} linhas - {first_row[:60]}")
            except:
                pass
        
        # Divs com "especificações" ou "características"
        print("\n⚙️ SEÇÕES DE SPECS:")
        specs = await page.query_selector_all('[class*="espec"], [class*="caract"], [class*="detail"], [class*="info"]')
        for i, spec in enumerate(specs[:5]):
            try:
                class_name = await spec.get_attribute('class')
                texto = await spec.inner_text()
                texto = texto.strip()[:100]
                if texto and len(texto) > 10:
                    print(f"  {i+1}. class='{class_name}': {texto}")
            except:
                pass
        
        # Salvar HTML
        html = await page.content()
        with open('analise_detalhes.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\n💾 HTML completo salvo em: analise_detalhes.html")
        
        await browser.close()
        print("\n✅ Análise concluída!")

asyncio.run(analisar_pagina())
