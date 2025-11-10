"""
Agente IA para comparação de preços usando Gemini Vision
Analisa screenshots de marketplaces e extrai produtos de forma inteligente
"""

from playwright.async_api import async_playwright
import asyncio
import base64
import os
import google.generativeai as genai
from marketplaces_config import get_all_marketplaces
import re
import json

class AIMarketplaceAgent:
    def __init__(self, gemini_api_key=None):
        self.playwright = None
        self.browser = None
        self.context = None
        
        # Configurar Gemini
        api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY não configurada! Configure em variável de ambiente ou passe como parâmetro.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')  # Modelo estável com visão
        
    async def iniciar(self):
        """Inicializar navegador"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
    async def buscar_produto(self, nome_produto, max_resultados=3):
        """
        Busca o produto em todos os marketplaces usando IA
        Retorna um dicionário com os resultados de cada marketplace
        """
        if not self.browser:
            await self.iniciar()
            
        print(f"\n🤖 Agente IA buscando: '{nome_produto}'")
        
        # Buscar em paralelo em todos os marketplaces
        marketplaces = get_all_marketplaces()
        tasks = []
        
        for marketplace_id, config in marketplaces.items():
            task = self._buscar_em_marketplace_com_ia(
                marketplace_id, 
                config, 
                nome_produto, 
                max_resultados
            )
            tasks.append(task)
            
        resultados = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Organizar resultados
        comparacao = {}
        for i, (marketplace_id, config) in enumerate(marketplaces.items()):
            if isinstance(resultados[i], Exception):
                print(f"  ❌ {config['nome']}: {resultados[i]}")
                comparacao[marketplace_id] = {
                    'nome': config['nome'],
                    'logo': config['logo'],
                    'cor': config['cor'],
                    'erro': str(resultados[i]),
                    'produtos': []
                }
            else:
                comparacao[marketplace_id] = resultados[i]
                
        return comparacao
    
    async def _buscar_em_marketplace_com_ia(self, marketplace_id, config, nome_produto, max_resultados):
        """Busca produtos usando IA para analisar a página"""
        try:
            print(f"  🛒 {config['nome']}...")
            
            page = await self.context.new_page()
            
            # Preparar query
            query = self._preparar_query(nome_produto)
            url_busca = config['url_busca'].format(query=query.replace(' ', '-'))
            
            # Navegar e aguardar carregamento
            await page.goto(url_busca, timeout=15000)
            await asyncio.sleep(3)  # Aguardar carregamento completo
            
            # Tirar screenshot
            screenshot_bytes = await page.screenshot(full_page=False)
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            # Pegar HTML para extração de links
            html_content = await page.content()
            
            await page.close()
            
            # Analisar com IA
            produtos = await self._analisar_com_ia(
                screenshot_b64,
                html_content,
                nome_produto,
                config['nome'],
                max_resultados
            )
            
            print(f"    ✅ {len(produtos)} produtos encontrados")
            
            return {
                'nome': config['nome'],
                'logo': config['logo'],
                'cor': config['cor'],
                'produtos': produtos,
                'url_busca': url_busca
            }
            
        except Exception as e:
            print(f"    ❌ Erro: {str(e)[:100]}")
            raise
    
    async def _analisar_com_ia(self, screenshot_b64, html_content, nome_produto, marketplace_nome, max_resultados):
        """Usa Gemini Vision para analisar a página e extrair produtos"""
        
        prompt = f"""Você é um especialista em e-commerce analisando resultados de busca.

TAREFA: Encontre os {max_resultados} MELHORES produtos que correspondem EXATAMENTE a: "{nome_produto}"

MARKETPLACE: {marketplace_nome}

INSTRUÇÕES CRÍTICAS:
1. Identifique apenas produtos IDÊNTICOS ao buscado (mesmo modelo, mesmas características)
2. Ignore acessórios, capas, películas, produtos similares
3. Para cada produto válido, extraia:
   - Título completo (exato como aparece)
   - Preço (apenas números, formato: 1234.56)

FORMATO DE RESPOSTA (JSON puro, sem markdown):
[
  {{
    "titulo": "Nome exato do produto",
    "preco": 1234.56
  }}
]

Se não encontrar produtos exatos, retorne: []

IMPORTANTE: Responda APENAS com o array JSON, sem explicações, sem markdown."""

        try:
            # Decodificar screenshot e criar PIL Image
            import io
            from PIL import Image
            screenshot_bytes = base64.b64decode(screenshot_b64)
            image = Image.open(io.BytesIO(screenshot_bytes))
            
            # Chamar Gemini Vision
            response = self.model.generate_content([prompt, image])
            
            # Extrair resposta
            resposta = response.text.strip()
            
            # Limpar markdown se existir
            if "```json" in resposta:
                resposta = resposta.split("```json")[1].split("```")[0].strip()
            elif "```" in resposta:
                resposta = resposta.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            produtos = json.loads(resposta)
            
            # Extrair links do HTML
            links_disponiveis = self._extrair_links_do_html(html_content, marketplace_nome)
            
            # Validar e formatar
            produtos_formatados = []
            for i, p in enumerate(produtos[:max_resultados]):
                if p.get('titulo') and p.get('preco'):
                    # Tentar encontrar link correspondente
                    link = self._encontrar_link_para_produto(p['titulo'], links_disponiveis)
                    
                    produtos_formatados.append({
                        'titulo': p['titulo'][:100],
                        'preco': float(p['preco']),
                        'preco_formatado': f"{float(p['preco']):.2f}",
                        'link': link or '#',
                        'imagem': None
                    })
            
            return produtos_formatados
            
        except Exception as e:
            print(f"      ⚠️ Erro na análise IA: {str(e)[:80]}")
            return []
    
    def _extrair_links_do_html(self, html_content, marketplace_nome):
        """Extrai todos os links de produtos do HTML"""
        import re
        
        # Padrões de URL por marketplace
        padroes = {
            'Mercado Livre': r'https://[^"\']*mercadolivre\.com\.br/[^"\']+',
            'Amazon Brasil': r'https://[^"\']*amazon\.com\.br/[^"\']+/dp/[^"\']+',
            'Shopee': r'https://[^"\']*shopee\.com\.br/[^"\']+',
            'Americanas': r'https://[^"\']*americanas\.com\.br/produto/[^"\']+',
            'Magazine Luiza': r'https://[^"\']*magazineluiza\.com\.br/[^"\']+/p/[^"\']+',
            'Casas Bahia': r'https://[^"\']*casasbahia\.com\.br/[^"\']+/p/[^"\']+',
            'KaBuM!': r'https://[^"\']*kabum\.com\.br/produto/[^"\']+',
            'Loja do Mecânico': r'https://[^"\']*lojadomecanico\.com\.br/[^"\']+'
        }
        
        padrao = padroes.get(marketplace_nome, r'https://[^"\']+')
        links = re.findall(padrao, html_content)
        
        # Limpar duplicatas e links inválidos
        links_limpos = []
        for link in links:
            if len(link) > 30 and link not in links_limpos:  # Links muito curtos provavelmente são inválidos
                links_limpos.append(link)
        
        return links_limpos[:20]  # Máximo 20 links
    
    def _encontrar_link_para_produto(self, titulo_produto, links_disponiveis):
        """Tenta encontrar o link mais adequado para um produto"""
        if not links_disponiveis:
            return None
        
        # Extrair palavras-chave do título
        palavras = re.findall(r'\w+', titulo_produto.lower())
        palavras = [p for p in palavras if len(p) > 3][:5]  # Máximo 5 palavras mais importantes
        
        # Pontuar cada link
        melhor_link = None
        melhor_pontuacao = 0
        
        for link in links_disponiveis:
            link_lower = link.lower()
            pontuacao = sum(1 for palavra in palavras if palavra in link_lower)
            
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_link = link
        
        return melhor_link if melhor_pontuacao > 0 else links_disponiveis[0]
    
    def _preparar_query(self, nome_produto):
        """Prepara a query de busca"""
        query = re.sub(r'[^\w\s-]', ' ', nome_produto)
        query = re.sub(r'\s+', ' ', query).strip()
        return query
    
    async def fechar(self):
        """Fechar navegador"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
