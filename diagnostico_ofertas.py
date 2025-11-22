import asyncio
from playwright.async_api import async_playwright

async def diagnosticar_estrutura():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("🔍 Acessando página de busca PS5...")
        await page.goto("https://www.comprasparaguai.com.br/busca/?q=ps5", wait_until="domcontentloaded")
        
        print("⏰ Aguardando carregar...")
        await asyncio.sleep(8)
        
        print("\n📜 Fazendo scroll...")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(3)
        
        # Verificar cards de ofertas
        print("\n🔍 Procurando cards de ofertas...")
        cards = await page.query_selector_all('.promocao-produtos-item')
        print(f"✓ Encontrou {len(cards)} cards")
        
        if len(cards) > 0:
            print("\n📋 Analisando primeiro card:")
            card = cards[0]
            
            # Pegar HTML do card
            html = await card.inner_html()
            print(f"\n--- HTML do Card (primeiros 500 chars) ---")
            print(html[:500])
            print("---\n")
            
            # Testar seletores
            print("🧪 Testando seletores:")
            
            # Loja
            loja_img = await card.query_selector('.store-image')
            if loja_img:
                alt = await loja_img.get_attribute('alt')
                src = await loja_img.get_attribute('src')
                print(f"  ✓ .store-image encontrado - alt: {alt}, src: {src[:50] if src else 'None'}...")
            else:
                print("  ✗ .store-image NÃO encontrado")
            
            # Preço
            preco_el = await card.query_selector('.promocao-item-preco-oferta strong')
            if preco_el:
                preco = await preco_el.inner_text()
                print(f"  ✓ .promocao-item-preco-oferta strong encontrado: {preco}")
            else:
                print("  ✗ .promocao-item-preco-oferta strong NÃO encontrado")
                # Tentar alternativas
                preco_alt = await card.query_selector('.promocao-item-preco-oferta')
                if preco_alt:
                    preco = await preco_alt.inner_text()
                    print(f"  ℹ️  .promocao-item-preco-oferta (sem strong): {preco}")
            
            # Nome do produto
            nome_el = await card.query_selector('.promocao-item-nome a')
            if nome_el:
                nome = await nome_el.inner_text()
                print(f"  ✓ .promocao-item-nome a encontrado: {nome[:50]}...")
            else:
                print("  ✗ .promocao-item-nome a NÃO encontrado")
            
            # Imagem
            img_el = await card.query_selector('.promocao-item-img img')
            if img_el:
                src = await img_el.get_attribute('src')
                data_src = await img_el.get_attribute('data-src')
                print(f"  ✓ .promocao-item-img img encontrado - src: {src[:50] if src else 'None'}...")
                print(f"    data-src: {data_src[:50] if data_src else 'None'}...")
            else:
                print("  ✗ .promocao-item-img img NÃO encontrado")
        
        print("\n⏸️  Aguardando 10 segundos para você ver a página...")
        await asyncio.sleep(10)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(diagnosticar_estrutura())
