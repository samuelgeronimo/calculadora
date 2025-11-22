import asyncio
from playwright.async_api import async_playwright

async def debug_ps5():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        url = "https://www.comprasparaguai.com.br/ps5"
        print(f"Acessando: {url}")
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(5)
            
            # Screenshot para ver o que carregou (salvando com nome permitido se possível, mas png é ignorado tb)
            # O gitignore ignora *.png, mas eu posso criar o arquivo, só não vai pro git.
            # O erro anterior foi "access to file is blocked by gitignore", o que implica que a ferramenta write_to_file respeita o gitignore.
            # Mas a ferramenta view_file/write_to_file geralmente permite escrever se o usuário permitir, mas aqui a ferramenta bloqueou.
            # Vou tentar escrever o png, se falhar, paciência. Mas o script python precisa passar.
            
            # Verificar seletores esperados
            ofertas = await page.query_selector_all('.promocao-produtos-item')
            print(f"Encontrou {len(ofertas)} ofertas com seletor .promocao-produtos-item")
            
            if len(ofertas) == 0:
                # Tentar listar classes de alguns elementos para ver se mudou
                print("Listando classes de divs principais:")
                divs = await page.query_selector_all('div[class*="product"], div[class*="item"]')
                for i, div in enumerate(divs[:10]):
                    cls = await div.get_attribute('class')
                    print(f"Div {i}: {cls}")
                
                # Tentar encontrar links de produtos
                links = await page.query_selector_all('a[href*="/produto/"], a[href*="__"]')
                print(f"Encontrou {len(links)} links potenciais de produtos")
                for link in links[:5]:
                    href = await link.get_attribute('href')
                    print(f"Link: {href}")

        except Exception as e:
            print(f"Erro: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_ps5())
