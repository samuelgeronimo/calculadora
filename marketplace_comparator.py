"""
Extrator de preços de múltiplos marketplaces brasileiros
"""

from playwright.async_api import async_playwright
import asyncio
import re
from marketplaces_config import get_all_marketplaces

# Dicionário de traduções comuns
TRADUCOES_CORES = {
    # Inglês -> Português
    'black': 'preto',
    'white': 'branco',
    'blue': 'azul',
    'red': 'vermelho',
    'green': 'verde',
    'yellow': 'amarelo',
    'purple': 'roxo',
    'pink': 'rosa',
    'orange': 'laranja',
    'gray': 'cinza',
    'grey': 'cinza',
    'silver': 'prata',
    'gold': 'dourado',
    'titanium': 'titânio',
    'natural': 'natural',
    'deep': 'profundo',
    'light': 'claro',
    'dark': 'escuro',
    'lavender': 'lavanda',
    'bloom': 'flor',
    'charcoal': 'carvão',
    'midnight': 'meia-noite',
    'glacier': 'glacial',
    # Português -> Inglês (para normalização)
    'preto': 'black',
    'branco': 'white',
    'azul': 'blue',
    'vermelho': 'red',
    'verde': 'green',
    'amarelo': 'yellow',
    'roxo': 'purple',
    'rosa': 'pink',
    'laranja': 'orange',
    'cinza': 'gray',
    'prata': 'silver',
    'dourado': 'gold',
    'titânio': 'titanium',
    'lavanda': 'lavender',
    'flor': 'bloom',
    'carvão': 'charcoal'
}

class MarketplaceComparator:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        
    async def iniciar(self):
        """Inicializar navegador"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
    async def buscar_produto(self, nome_produto, max_resultados=3):
        """
        Busca o produto em todos os marketplaces
        Retorna um dicionário com os resultados de cada marketplace
        """
        if not self.browser:
            await self.iniciar()
            
        print(f"\n🔍 Buscando '{nome_produto}' em marketplaces brasileiros...")
        
        # Preparar query de busca
        query = self._preparar_query(nome_produto)
        
        # Extrair palavras-chave do produto original para validação
        self.produto_original = nome_produto
        self.palavras_chave = self._extrair_palavras_chave(nome_produto)
        
        print(f"   📌 Palavras-chave: {', '.join(sorted(self.palavras_chave)[:10])}...")
        
        # Buscar em paralelo em todos os marketplaces
        marketplaces = get_all_marketplaces()
        tasks = []
        
        for marketplace_id, config in marketplaces.items():
            task = self._buscar_em_marketplace(marketplace_id, config, query, max_resultados)
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
    
    def _extrair_palavras_chave(self, nome_produto):
        """Extrai palavras-chave importantes do nome do produto"""
        # Normalizar texto
        texto = nome_produto.lower()
        
        # Remover palavras comuns que não são relevantes
        palavras_irrelevantes = ['o', 'a', 'de', 'da', 'do', 'e', 'para', 'com', 'em', '-', '–', 'the']
        
        # Extrair palavras
        palavras = re.findall(r'\w+', texto)
        
        # Filtrar palavras importantes
        palavras_importantes = []
        for palavra in palavras:
            # Incluir palavras com 2+ caracteres (para pegar "gb", "tb", números, etc)
            if len(palavra) >= 2 and palavra not in palavras_irrelevantes:
                palavras_importantes.append(palavra)
                # Adicionar tradução se existir
                if palavra in TRADUCOES_CORES:
                    palavras_importantes.append(TRADUCOES_CORES[palavra])
        
        return set(palavras_importantes)
    
    def _validar_produto(self, titulo_produto):
        """
        Valida se o produto encontrado corresponde ao produto buscado
        Retorna True se for uma correspondência válida
        """
        if not titulo_produto:
            return False
        
        # Normalizar título e produto original
        titulo_lower = titulo_produto.lower()
        produto_original_lower = self.produto_original.lower()
        
        # Converter cores em inglês para português e vice-versa
        for en, pt in TRADUCOES_CORES.items():
            titulo_lower = titulo_lower.replace(en, pt)
            produto_original_lower = produto_original_lower.replace(en, pt)
        
        # REGRA 1: Validação de números de modelo (CRÍTICA - apenas para produtos com números)
        # Extrair números do produto original e do título
        numeros_originais = re.findall(r'\d+', self.produto_original)
        numeros_titulo = re.findall(r'\d+', titulo_produto)
        
        # Se o produto original tem números importantes (modelo), DEVE ter os mesmos no título
        if numeros_originais:
            # Verificar números críticos (modelos de celular, capacidade)
            numeros_criticos = [n for n in numeros_originais if len(n) >= 2]  # 15, 17, 256, etc
            
            # Apenas aplicar regra se tiver números críticos
            if numeros_criticos:
                for numero in numeros_criticos:
                    # Exceção: capacidades podem variar (128, 256, 512, 1024)
                    if numero in ['128', '256', '512', '1024', '1', '2']:
                        continue
                        
                    # Número de modelo DEVE estar presente
                    if numero not in numeros_titulo:
                        return False
        
        # REGRA 2: Contar quantas palavras-chave importantes estão presentes
        palavras_encontradas = 0
        palavras_obrigatorias = ['iphone', 'galaxy', 'xiaomi', 'samsung', 'motorola', 'apple', 'echo', 'alexa', 'google', 'nest', 'dot']
        
        for palavra in self.palavras_chave:
            if palavra in titulo_lower:
                palavras_encontradas += 1
                
        # REGRA 3: Verificar se tem pelo menos uma palavra obrigatória (marca/modelo)
        tem_palavra_obrigatoria = any(palavra in titulo_lower for palavra in palavras_obrigatorias if palavra in self.palavras_chave)
        
        if not tem_palavra_obrigatoria:
            return False
        
        # REGRA 4: Calcular percentual de correspondência
        total_palavras = len(self.palavras_chave)
        if total_palavras == 0:
            return False
            
        percentual = (palavras_encontradas / total_palavras) * 100
        
        # Para produtos sem números (como Echo Pop), ser mais flexível
        # Exigir 50% se não tem números críticos, 60% se tem
        minimo_requerido = 60 if numeros_criticos else 50
        
        return percentual >= minimo_requerido
        
    def _preparar_query(self, nome_produto):
        """Prepara a query de busca removendo caracteres especiais"""
        # Remover caracteres especiais e normalizar
        query = re.sub(r'[^\w\s-]', ' ', nome_produto)
        query = re.sub(r'\s+', ' ', query).strip()
        # URL encode será feito no momento da busca
        return query
        
    async def _buscar_em_marketplace(self, marketplace_id, config, query, max_resultados):
        """Busca produtos em um marketplace específico"""
        try:
            print(f"  🛒 Buscando em {config['nome']}...")
            
            page = await self.context.new_page()
            
            # Montar URL de busca
            url_busca = config['url_busca'].format(query=query.replace(' ', '-'))
            
            # Navegar para a página de busca
            await page.goto(url_busca, wait_until='domcontentloaded', timeout=15000)
            await asyncio.sleep(2)  # Aguardar carregamento dinâmico
            
            # Extrair produtos
            produtos = await self._extrair_produtos(page, config['seletores'], max_resultados)
            
            await page.close()
            
            print(f"    ✅ {len(produtos)} produtos encontrados")
            
            return {
                'nome': config['nome'],
                'logo': config['logo'],
                'cor': config['cor'],
                'produtos': produtos,
                'url_busca': url_busca
            }
            
        except Exception as e:
            print(f"    ❌ Erro: {e}")
            raise
            
    async def _extrair_produtos(self, page, seletores, max_resultados):
        """Extrai produtos de uma página usando os seletores configurados"""
        produtos = []
        produtos_validados = 0
        
        try:
            # Aguardar container
            await page.wait_for_selector(seletores['item'], timeout=5000)
            
            # Pegar todos os itens (buscar mais para compensar filtros)
            items = await page.query_selector_all(seletores['item'])
            
            # Processar até ter produtos suficientes ou acabarem os itens
            for item in items:
                if produtos_validados >= max_resultados:
                    break
                    
                try:
                    produto = {}
                    
                    # Título
                    titulo_elem = await item.query_selector(seletores['titulo'])
                    if titulo_elem:
                        produto['titulo'] = await titulo_elem.inner_text()
                        produto['titulo'] = produto['titulo'].strip()[:100]
                    
                    # Validar se o produto corresponde ao buscado
                    if not produto.get('titulo') or not self._validar_produto(produto['titulo']):
                        # Debug: mostrar produtos rejeitados
                        if produto.get('titulo'):
                            print(f"      ✗ Rejeitado: {produto['titulo'][:60]}...")
                        continue  # Pular produto que não corresponde
                    
                    # Preço
                    preco_elem = await item.query_selector(seletores['preco'])
                    if preco_elem:
                        preco_text = await preco_elem.inner_text()
                        produto['preco'] = self._extrair_preco(preco_text)
                        produto['preco_formatado'] = preco_text.strip()
                    
                    # Link
                    link_elem = await item.query_selector(seletores['link'])
                    if link_elem:
                        href = await link_elem.get_attribute('href')
                        if href and not href.startswith('http'):
                            # URL relativa, completar
                            href = page.url.split('/')[0] + '//' + page.url.split('/')[2] + href
                        produto['link'] = href
                    
                    # Imagem
                    img_elem = await item.query_selector(seletores['imagem'])
                    if img_elem:
                        src = await img_elem.get_attribute('src')
                        if not src:
                            src = await img_elem.get_attribute('data-src')
                        produto['imagem'] = src
                    
                    # Só adicionar se tiver título, preço E passar na validação
                    if produto.get('titulo') and produto.get('preco'):
                        produtos.append(produto)
                        produtos_validados += 1
                        print(f"      ✓ Validado: {produto['titulo'][:60]}...")
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"      ⚠️ Erro ao extrair produtos: {e}")
            
        return produtos
        
    def _extrair_preco(self, preco_text):
        """Extrai valor numérico do preço"""
        try:
            # Remover tudo exceto números e vírgula/ponto
            preco = re.sub(r'[^\d,.]', '', preco_text)
            # Substituir vírgula por ponto
            preco = preco.replace('.', '').replace(',', '.')
            return float(preco)
        except:
            return 0.0
            
    async def fechar(self):
        """Fechar navegador"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
