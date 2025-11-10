import asyncio
from playwright.async_api import async_playwright

async def analisar():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        url = "https://www.comprasparaguai.com.br/console-xbox-series-x-1tb-8k-1882__5005772/"
        print(f"🔍 Acessando: {url}")
        await page.goto(url, wait_until='domcontentloaded')
        await asyncio.sleep(5)
        
        # Salvar HTML completo
        html = await page.content()
        with open('analise_star_games.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ HTML salvo em analise_star_games.html")
        
        # Procurar block-paragraph
        paragraphs = await page.query_selector_all('.block-paragraph')
        print(f"\n📝 Encontrados {len(paragraphs)} elementos .block-paragraph:")
        for i, p in enumerate(paragraphs, 1):
            text = await p.inner_text()
            text = text.strip()
            print(f"\n--- Parágrafo {i} ({len(text)} chars) ---")
            print(text[:200] if len(text) > 200 else text)
        
        await browser.close()

asyncio.run(analisar())
