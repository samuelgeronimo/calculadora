"""
Análise do HTML para debug
"""
import asyncio
from playwright.async_api import async_playwright

async def analyze():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        # Simular exatamente o que o Flask faz
        await page.goto("https://www.comprasparaguai.com.br", timeout=90000, wait_until="domcontentloaded")
        await asyncio.sleep(2)
        
        search_input = await page.wait_for_selector('input[name="q"]', timeout=10000)
        await search_input.fill("xbox")
        await search_input.press("Enter")
        
        # Wait networkidle como no código atualizado
        await page.wait_for_load_state('networkidle', timeout=30000)
        await asyncio.sleep(2)
        
        # Rolar como no extrair_filtros
        for i in range(3):
            await page.evaluate(f"window.scrollBy(0, 200)")
            await asyncio.sleep(0.3)
        await asyncio.sleep(2)
        
        # Analisar
        info = await page.evaluate("""() => {
            return {
                url: window.location.href,
                title: document.title,
                ctgSuggestions: !!document.querySelector('.ctg-suggestions'),
                ctgSuggestionsList: !!document.querySelector('.ctg-suggestions-list'),
                jsSuggestionList: !!document.querySelector('.js-suggestion-list'),
                ctgSuggestionsClass: document.querySelector('.ctg-suggestions')?.className || 'N/A',
                ctgSuggestionsDisplay: document.querySelector('.ctg-suggestions') ? window.getComputedStyle(document.querySelector('.ctg-suggestions')).display : 'N/A',
                linksCount: document.querySelector('.ctg-suggestions')?.querySelectorAll('a').length || 0,
                firstLink: document.querySelector('.ctg-suggestions a')?.innerText || 'N/A'
            };
        }""")
        
        print("\n" + "="*70)
        print("ANÁLISE PÓS-BUSCA (simulando Flask)")
        print("="*70)
        print(f"URL: {info['url']}")
        print(f"Title: {info['title']}")
        print(f"\nElementos:")
        print(f"  .ctg-suggestions existe: {info['ctgSuggestions']}")
        print(f"  .ctg-suggestions-list existe: {info['ctgSuggestionsList']}")
        print(f"  .js-suggestion-list existe: {info['jsSuggestionList']}")
        print(f"  .ctg-suggestions classe: {info['ctgSuggestionsClass']}")
        print(f"  .ctg-suggestions display: {info['ctgSuggestionsDisplay']}")
        print(f"  Links: {info['linksCount']}")
        print(f"  Primeiro link: {info['firstLink']}")
        
        await browser.close()

asyncio.run(analyze())
