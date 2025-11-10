"""
Descobrir o seletor correto dos produtos
"""
import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        print("Navegando para Games...")
        await page.goto("https://www.comprasparaguai.com.br/games/?q=ps5", wait_until="domcontentloaded")
        await asyncio.sleep(5)
        
        print("\nProcurando seletores de produtos...")
        result = await page.evaluate("""() => {
            const seletores = [
                '.box--item',
                '.item-produto',
                '.product-item',
                '[class*="item"]',
                '[class*="product"]',
                '[class*="box"]'
            ];
            
            const resultados = {};
            seletores.forEach(sel => {
                const elementos = document.querySelectorAll(sel);
                resultados[sel] = elementos.length;
            });
            
            // Procurar classes que contém "item" ou "product"
            const allDivs = document.querySelectorAll('div[class*="item"], div[class*="product"], div[class*="box"]');
            const classes = new Set();
            allDivs.forEach(div => {
                if (div.className) {
                    div.className.split(' ').forEach(cls => {
                        if (cls.includes('item') || cls.includes('product') || cls.includes('box')) {
                            classes.add(cls);
                        }
                    });
                }
            });
            
            resultados['classes_encontradas'] = Array.from(classes).slice(0, 20);
            
            return resultados;
        }""")
        
        print("\n📊 Resultados:")
        for seletor, count in result.items():
            if seletor != 'classes_encontradas':
                print(f"  {seletor}: {count} elementos")
        
        print("\n🏷️ Classes encontradas com 'item', 'product' ou 'box':")
        for cls in result['classes_encontradas']:
            print(f"  - {cls}")
        
        # Tentar pegar exemplo de produto
        print("\n🔍 Tentando extrair exemplo de produto...")
        exemplo = await page.evaluate("""() => {
            // Tentar múltiplos seletores
            const seletores = [
                '.box--item',
                '[class*="item-"]',
                'div[class*="product"]',
                'article',
                '.item'
            ];
            
            for (const sel of seletores) {
                const item = document.querySelector(sel);
                if (item) {
                    return {
                        seletor: sel,
                        html: item.outerHTML.substring(0, 500),
                        texto: item.innerText.substring(0, 200)
                    };
                }
            }
            return null;
        }""")
        
        if exemplo:
            print(f"\n✅ Encontrou com seletor: {exemplo['seletor']}")
            print(f"Texto: {exemplo['texto'][:100]}")
        else:
            print("\n❌ Nenhum produto encontrado")
        
        input("\nPressione ENTER para fechar...")
        await browser.close()

asyncio.run(test())
