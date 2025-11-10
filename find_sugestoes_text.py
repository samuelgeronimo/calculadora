"""
Procurar pelo texto "Sugestões" e extrair links próximos
"""
import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        await page.goto("https://www.comprasparaguai.com.br/busca/?q=ps5", wait_until="domcontentloaded")
        await asyncio.sleep(5)
        
        print("Procurando elementos com texto 'Sugestões'...")
        result = await page.evaluate("""() => {
            // Procurar por qualquer elemento que contenha "Sugestões"
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                null
            );
            
            const suggestions = [];
            let node;
            
            while (node = walker.nextNode()) {
                if (node.textContent.includes('Sugestões') || node.textContent.includes('Sugestoes')) {
                    let parent = node.parentElement;
                    while (parent && parent !== document.body) {
                        const links = parent.querySelectorAll('a');
                        if (links.length > 0) {
                            suggestions.push({
                                tag: parent.tagName,
                                className: parent.className,
                                linksCount: links.length,
                                links: Array.from(links).slice(0, 5).map(a => a.innerText.trim())
                            });
                            break;
                        }
                        parent = parent.parentElement;
                    }
                    break;
                }
            }
            
            return suggestions;
        }""")
        
        if len(result) > 0:
            print(f"\n✅ Encontrado container com 'Sugestões'!")
            for item in result:
                print(f"\nTag: {item['tag']}")
                print(f"Classe: {item['className']}")
                print(f"Total de links: {item['linksCount']}")
                print(f"Primeiros links:")
                for link in item['links']:
                    print(f"  - {link}")
        else:
            print("\n❌ Texto 'Sugestões' não encontrado")
            
            # Salvar HTML para análise
            html = await page.content()
            with open('page_content.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("\n💾 HTML salvo em page_content.html para análise")
        
        await browser.close()

asyncio.run(test())
