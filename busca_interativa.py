"""
Script interativo para aplicar filtros na busca de produtos no comprasparaguai.com.br
"""

import asyncio
from playwright.async_api import async_playwright
import json


class ComprasParaguaiBusca:
    """Classe para gerenciar busca e filtros no site comprasparaguai.com.br"""
    
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None
        self.base_url = "https://www.comprasparaguai.com.br"
        
    async def iniciar_navegador(self, headless=False):
        """Inicia o navegador"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless, slow_mo=500)
        self.page = await self.browser.new_page()
        # Aumentar timeout padrão
        self.page.set_default_timeout(90000)
        
    async def fechar_navegador(self):
        """Fecha o navegador"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright') and self.playwright:
            await self.playwright.stop()
    
    async def buscar_produto(self, termo_busca):
        """
        Realiza busca por um produto
        
        Args:
            termo_busca: Termo a ser pesquisado
        """
        print(f"🌐 Navegando para {self.base_url}...")
        try:
            await self.page.goto(self.base_url, timeout=90000, wait_until="domcontentloaded")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"⚠️ Timeout ao carregar página, continuando mesmo assim...")
        
        print(f"🔍 Buscando por '{termo_busca}'...")
        search_input = await self.page.wait_for_selector('input[name="q"]', timeout=10000)
        await search_input.fill(termo_busca)
        await search_input.press("Enter")
        
        await asyncio.sleep(3)
        print(f"✅ Busca realizada com sucesso!")
        
    async def aplicar_filtro_loja(self, loja):
        """
        Aplica filtro de loja
        
        Args:
            loja: Nome da loja (ex: 'Atacado Connect')
        """
        print(f"🏪 Aplicando filtro de loja: {loja}...")
        
        # Procurar pelo checkbox da loja
        checkbox_selector = f'input[id="filtro-{loja}"]'
        try:
            # Rolar até o filtro para torná-lo visível
            checkbox = await self.page.wait_for_selector(checkbox_selector, state="attached", timeout=5000)
            await checkbox.scroll_into_view_if_needed()
            await asyncio.sleep(0.5)
            
            # Clicar usando JavaScript se necessário
            await self.page.evaluate(f"""
                document.querySelector('input[id="filtro-{loja}"]').click()
            """)
            await asyncio.sleep(2)
            print(f"✅ Filtro de loja aplicado!")
        except Exception as e:
            print(f"⚠️ Não foi possível aplicar filtro de loja: {str(e)}")
    
    async def aplicar_filtro_marca(self, marca):
        """
        Aplica filtro de marca
        
        Args:
            marca: Nome da marca (ex: 'Sony')
        """
        print(f"🏷️ Aplicando filtro de marca: {marca}...")
        
        checkbox_selector = f'input[id="filtro-{marca}"]'
        try:
            # Rolar até o filtro para torná-lo visível
            checkbox = await self.page.wait_for_selector(checkbox_selector, state="attached", timeout=5000)
            await checkbox.scroll_into_view_if_needed()
            await asyncio.sleep(0.5)
            
            # Clicar usando JavaScript se necessário
            await self.page.evaluate(f"""
                document.querySelector('input[id="filtro-{marca}"]').click()
            """)
            await asyncio.sleep(2)
            print(f"✅ Filtro de marca aplicado!")
        except Exception as e:
            print(f"⚠️ Não foi possível aplicar filtro de marca: {str(e)}")
    
    async def ordenar_por(self, criterio):
        """
        Ordena resultados por critério
        
        Args:
            criterio: Critério de ordenação (Relevância, Menor Preço, Maior Preço, etc)
        """
        print(f"📊 Ordenando por: {criterio}...")
        
        try:
            # Encontrar o select de ordenação
            select = await self.page.wait_for_selector('select', timeout=5000)
            await select.select_option(label=criterio)
            await asyncio.sleep(2)
            print(f"✅ Ordenação aplicada!")
        except Exception as e:
            print(f"⚠️ Não foi possível aplicar ordenação: {str(e)}")
    
    async def capturar_resultados(self):
        """Captura e exibe os resultados da busca"""
        print(f"\n📦 Capturando resultados...")
        
        # Rolar para ver mais produtos
        for i in range(3):
            await self.page.evaluate(f"window.scrollBy(0, {400 * (i + 1)})")
            await asyncio.sleep(0.5)
        
        # Capturar produtos
        try:
            produtos = await self.page.query_selector_all('.product-item, .produto-item, [class*="product"]')
            print(f"✅ Encontrados {len(produtos)} produtos na página")
            
            # Tentar extrair informações dos produtos
            produtos_info = []
            for i, produto in enumerate(produtos[:10]):  # Primeiros 10 produtos
                try:
                    texto = await produto.inner_text()
                    if len(texto) > 20:  # Filtrar elementos vazios
                        produtos_info.append(texto[:200])  # Primeiros 200 caracteres
                except:
                    pass
            
            if produtos_info:
                print(f"\n🛒 PRODUTOS ENCONTRADOS:")
                for i, info in enumerate(produtos_info, 1):
                    print(f"\n{i}. {info}")
                    print("-" * 60)
            
            # Salvar screenshot
            await self.page.screenshot(path="c:\\dev\\calculadora\\resultados_filtrados.png")
            print(f"\n📸 Screenshot salvo: resultados_filtrados.png")
            
        except Exception as e:
            print(f"⚠️ Erro ao capturar produtos: {str(e)}")


async def exemplo_uso_basico():
    """Exemplo básico de uso"""
    busca = ComprasParaguaiBusca()
    
    try:
        await busca.iniciar_navegador(headless=False)
        
        # 1. Buscar por PS5
        await busca.buscar_produto("ps5")
        
        # 2. Aplicar filtro de marca Sony
        await busca.aplicar_filtro_marca("Sony")
        
        # 3. Ordenar por menor preço
        await busca.ordenar_por("Menor Preço")
        
        # 4. Capturar resultados
        await busca.capturar_resultados()
        
        # Manter navegador aberto
        print(f"\n⏳ Mantendo navegador aberto por 15 segundos...")
        await asyncio.sleep(15)
        
    finally:
        await busca.fechar_navegador()


async def busca_interativa():
    """Modo interativo para aplicar filtros personalizados"""
    
    # Carregar filtros extraídos anteriormente
    try:
        with open("c:\\dev\\calculadora\\filtros_extraidos.json", "r", encoding="utf-8") as f:
            filtros_data = json.load(f)
    except:
        print("⚠️ Arquivo filtros_extraidos.json não encontrado. Execute primeiro playwright_search.py")
        return
    
    busca = ComprasParaguaiBusca()
    
    try:
        await busca.iniciar_navegador(headless=False)
        
        # Buscar por PS5
        await busca.buscar_produto("ps5")
        
        print("\n" + "="*60)
        print("🎯 FILTROS DISPONÍVEIS")
        print("="*60)
        
        # Mostrar lojas disponíveis
        lojas = filtros_data.get("checkboxes", [])[:20]
        print(f"\n🏪 LOJAS DISPONÍVEIS:")
        for i, loja in enumerate(lojas, 1):
            print(f"   {i}. {loja}")
        
        # Mostrar marcas (extraídas do JSON)
        marcas = ["Sony", "Nacon", "Razer", "Logitech", "Kingston", "Redragon", "JBL", "SteelSeries"]
        print(f"\n🏷️ MARCAS DISPONÍVEIS:")
        for i, marca in enumerate(marcas, 1):
            print(f"   {i}. {marca}")
        
        # Mostrar opções de ordenação
        ordenacoes = filtros_data.get("selects", [{}])[0].get("opcoes", [])
        print(f"\n📊 ORDENAÇÃO DISPONÍVEL:")
        for i, ordem in enumerate(ordenacoes, 1):
            print(f"   {i}. {ordem}")
        
        print("\n" + "="*60)
        print("💡 EXEMPLOS DE USO NO CÓDIGO:")
        print("="*60)
        print("""
# Para aplicar filtro de marca Sony:
await busca.aplicar_filtro_marca("Sony")

# Para aplicar filtro de loja:
await busca.aplicar_filtro_loja("Atacado Connect")

# Para ordenar por menor preço:
await busca.ordenar_por("Menor Preço")

# Para capturar resultados:
await busca.capturar_resultados()
        """)
        
        # Aplicar alguns filtros como exemplo
        print("\n🔧 Aplicando filtros de exemplo...")
        
        # Filtrar por marca Sony
        await busca.aplicar_filtro_marca("Sony")
        
        # Ordenar por menor preço
        await busca.ordenar_por("Menor Preço")
        
        # Capturar resultados
        await busca.capturar_resultados()
        
        # Manter navegador aberto
        print(f"\n⏳ Mantendo navegador aberto por 20 segundos para você explorar...")
        await asyncio.sleep(20)
        
    finally:
        await busca.fechar_navegador()


if __name__ == "__main__":
    print("🚀 Iniciando busca interativa no comprasparaguai.com.br")
    print("=" * 60)
    
    # Execute a busca interativa
    asyncio.run(busca_interativa())
    
    # Ou use o exemplo básico:
    # asyncio.run(exemplo_uso_basico())
