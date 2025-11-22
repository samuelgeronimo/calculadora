import asyncio
from app import ProductExtractor

async def main():
    extractor = ProductExtractor()
    await extractor.iniciar()
    
    url = "https://www.comprasparaguai.com.br/busca/?q=ps5"
    print(f"Acessando {url}...")
    
    try:
        await extractor.page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(5) # Wait for dynamic content
        
        # Save HTML for inspection
        content = await extractor.page.content()
        with open("inspect_ps5_search.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("HTML salvo em inspect_ps5_search.html")
        
        # Try to find "Sugestões de categorias" text
        # It might be in a div or header
        
        # Look for elements containing "Sugestões de categorias"
        elements = await extractor.page.query_selector_all("text=Sugestões de categorias")
        if elements:
            print(f"Encontrado {len(elements)} elementos com texto 'Sugestões de categorias'")
            for i, el in enumerate(elements):
                # Get parent to see structure
                parent = await el.evaluate("el => el.parentElement.outerHTML")
                print(f"Parent {i}: {parent[:500]}...")
        else:
            print("Texto 'Sugestões de categorias' não encontrado diretamente.")
            
        # Look for common category selectors
        cats = await extractor.page.query_selector_all(".ctg-suggestions")
        if cats:
            print("Encontrado .ctg-suggestions")
            html = await cats[0].inner_html()
            print(html[:500])
            
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        await extractor.fechar()

if __name__ == "__main__":
    asyncio.run(main())
