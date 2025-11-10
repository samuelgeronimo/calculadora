"""
Buscar qualquer elemento com "suggestion" no nome da classe
"""
import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        await page.goto("https://www.comprasparaguai.com.br/busca/?q=ps5", wait_until="domcontentloaded")
        await asyncio.sleep(5)
        
        print("Procurando elementos com 'suggest' ou 'categ' na classe...")
        result = await page.evaluate("""() => {
            const allElements = document.querySelectorAll('*');
            const matches = [];
            
            allElements.forEach(el => {
                const className = el.className;
                if (typeof className === 'string' && 
                    (className.includes('suggest') || className.includes('categ'))) {
                    const links = el.querySelectorAll('a');
                    if (links.length > 0) {
                        matches.push({
                            tag: el.tagName,
                            className: className,
                            linksCount: links.length,
                            firstLink: links[0]?.innerText.substring(0, 50) || 'N/A'
                        });
                    }
                }
            });
            
            return matches.slice(0, 10);
        }""")
        
        print(f"\n✅ Elementos encontrados: {len(result)}\n")
        for idx, elem in enumerate(result, 1):
            print(f"{idx}. <{elem['tag']}> class=\"{elem['className']}\"")
            print(f"   Links: {elem['linksCount']}, Primeiro: {elem['firstLink']}")
            print()
        
        await browser.close()

asyncio.run(test())
