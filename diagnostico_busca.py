import asyncio
from playwright.async_api import async_playwright

async def debug_busca():
    log_content = []
    def log(msg):
        print(msg)
        log_content.append(str(msg))

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        log("Acessando home...")
        await page.goto("https://www.comprasparaguai.com.br/", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        log("Tentando buscar 'ps5'...")
        # Tentar encontrar o input de busca
        input_selector = 'input[name="q"], input[type="search"], #search, .search-input'
        try:
            await page.fill(input_selector, "ps5")
            await page.press(input_selector, "Enter")
            
            log("Aguardando navegação...")
            await page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(5)
            
            log(f"URL Final: {page.url}")
            
            # Salvar HTML da página de resultados
            content = await page.content()
            with open("busca_result.html", "w", encoding="utf-8") as f:
                f.write(content)
            log("HTML salvo em busca_result.html")

            # Procurar cards
            cards = await page.query_selector_all('.promocao-produtos-item')
            log(f"Seletor antigo (.promocao-produtos-item) encontrou: {len(cards)}")
            
            # Tentar descobrir novo seletor
            log("Procurando classes de elementos que parecem produtos...")
            # Buscar divs que tenham imagem e preço
            items = await page.evaluate('''() => {
                const results = [];
                const divs = document.querySelectorAll('div');
                for (const div of divs) {
                    const txt = div.innerText || '';
                    if (txt.includes('US$') && div.querySelector('img')) {
                        results.push({cls: div.className, txt: txt.substring(0, 30)});
                    }
                }
                return results.slice(0, 20);
            }''')
            
            for item in items:
                log(f"Candidato: {item}")
                
        except Exception as e:
            log(f"Erro na busca: {e}")
            
        finally:
            await browser.close()
            with open("log_busca.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(log_content))

if __name__ == "__main__":
    asyncio.run(debug_busca())
