import asyncio
import secrets
import requests
from threading import Thread
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from playwright.async_api import async_playwright

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Chave secreta para sessões

# Armazenamento temporário de dados de detalhes
detalhes_temp = {}

def obter_cotacao_dolar():
    """Obter cotação atual do dólar via API + 10 centavos"""
    try:
        # Usando API pública do Banco Central do Brasil
        response = requests.get('https://economia.awesomeapi.com.br/json/last/USD-BRL', timeout=5)
        if response.status_code == 200:
            data = response.json()
            cotacao_base = float(data['USDBRL']['bid'])
            cotacao_final = cotacao_base + 0.10  # Adiciona 10 centavos
            print(f"💵 Cotação do dólar (API): R$ {cotacao_base:.2f}")
            print(f"💵 Cotação final (+R$ 0,10): R$ {cotacao_final:.2f}")
            return cotacao_final
        return 5.60  # Valor padrão caso a API falhe (já com os 10 centavos)
    except Exception as e:
        print(f"⚠️ Erro ao obter cotação do dólar: {e}")
        return 5.60  # Valor padrão (já com os 10 centavos)

# Event loop global
event_loop = None
loop_thread = None

def get_event_loop():
    global event_loop, loop_thread
    if event_loop is None:
        def run_loop():
            global event_loop
            event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop)
            event_loop.run_forever()
        loop_thread = Thread(target=run_loop, daemon=True)
        loop_thread.start()
        import time
        while event_loop is None:
            time.sleep(0.01)
    return event_loop

def run_async(coro):
    loop = get_event_loop()
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result()


class ProductExtractor:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
    
    async def iniciar(self):
        """Inicializar o Playwright e navegador"""
        print("🚀 Iniciando Playwright...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page(viewport={'width': 1920, 'height': 1080})
        print("✅ Navegador iniciado")
    
    async def extrair_texto_seletor(self, selectors):
        """Tentar extrair texto de uma lista de seletores"""
        for sel in selectors:
            try:
                if sel.startswith('meta'):
                    el = await self.page.query_selector(sel)
                    if el:
                        content = await el.get_attribute('content')
                        if content and content.strip():
                            print(f"    ✓ Seletor '{sel}' encontrou: {content.strip()[:80]}")
                            return content.strip()
                else:
                    el = await self.page.query_selector(sel)
                    if el:
                        text = await el.inner_text()
                        if text and text.strip():
                            print(f"    ✓ Seletor '{sel}' encontrou: {text.strip()[:80]}")
                            return text.strip()
            except Exception as e:
                print(f"    ✗ Seletor '{sel}' falhou: {e}")
                continue
        print(f"    ⚠️ Nenhum seletor funcionou de {len(selectors)} tentativas")
        return ''
    
    async def extrair_produto(self, url):
        """Extrair informações do produto de uma URL"""
        try:
            print(f"🔍 Acessando: {url}")
            await self.page.goto(url, wait_until="networkidle", timeout=60000)
            await asyncio.sleep(8)  # Aguardar mais tempo para JavaScript carregar
            
            # Extrair título
            titulo = await self.extrair_texto_seletor([
                'meta[property="og:title"]',
                'h1.page-title span',
                'h1.page-title',
                'h1.product-title',
                'h1.product-name',
                'h1[itemprop="name"]',
                '.product-name h1',
                '.page-title span.base',
                'h1 span.base'
            ])
            print(f"  📝 Título extraído: {titulo}")
            
            # Extrair preço
            preco = await self.extrair_texto_seletor([
                '.price-wrapper .price',
                'span[data-price-type="finalPrice"] .price',
                '.product-info-price .price',
                '.product-price',
                '[itemprop="price"]',
                'span.price',
                '.price',
                '.sale-price'
            ])
            print(f"  💰 Preço extraído: {preco}")
            
            # Extrair descrição
            descricao = await self.extrair_texto_seletor([
                '.product-description',
                '[itemprop="description"]',
                '.description',
                'meta[name="description"]',
                '.product-info-description',
                '#description',
                '.value[itemprop="description"]'
            ])
            
            # Extrair marca - primeiro dos seletores, depois da tabela
            marca = await self.extrair_texto_seletor([
                '.product-brand',
                '[itemprop="brand"]',
                '.brand-name',
                'meta[property="product:brand"]'
            ])
            
            # Se não encontrou marca, buscar na tabela
            if not marca:
                rows = await self.page.query_selector_all('tr')
                for row in rows:
                    try:
                        th = await row.query_selector('th')
                        if th:
                            th_text = await th.inner_text()
                            if 'marca' in th_text.lower():
                                td = await row.query_selector('td')
                                if td:
                                    marca = await td.inner_text()
                                    marca = marca.strip()
                                    break
                    except:
                        continue
            
            # Extrair detalhes técnicos
            detalhes = []
            rows = await self.page.query_selector_all('tr')
            for row in rows[:20]:  # Limitar a 20 linhas
                try:
                    th = await row.query_selector('th')
                    td = await row.query_selector('td')
                    if th and td:
                        nome = await th.inner_text()
                        valor = await td.inner_text()
                        if nome.strip() and valor.strip() and nome.strip() != valor.strip():
                            detalhes.append({
                                'nome': nome.strip().replace(':', ''),
                                'valor': valor.strip()
                            })
                except:
                    continue
            
            # Extrair fotos
            fotos = []
            fotos_set = set()
            
            # Tentar seletores específicos
            img_selectors = [
                '.product-image img',
                '.product-gallery img',
                '[itemprop="image"]',
                '.gallery-image img',
                'img.product-img',
                '.product-media img',
                '.fotorama img',
                '.gallery img'
            ]
            
            for sel in img_selectors:
                try:
                    imgs = await self.page.query_selector_all(sel)
                    for img in imgs:
                        src = await img.get_attribute('src')
                        if not src:
                            src = await img.get_attribute('data-src')
                        if not src:
                            src = await img.get_attribute('data-original')
                        if src and 'data:image' not in src and len(src) > 20:
                            fotos_set.add(src)
                except:
                    continue
            
            # Se não encontrou, pegar meta og:image
            if not fotos_set:
                try:
                    meta = await self.page.query_selector('meta[property="og:image"]')
                    if meta:
                        content = await meta.get_attribute('content')
                        if content:
                            fotos_set.add(content)
                except:
                    pass
            
            # Se ainda não encontrou, pegar todas as imagens grandes
            if not fotos_set:
                try:
                    all_imgs = await self.page.query_selector_all('img')
                    for img in all_imgs[:30]:  # Limitar busca
                        try:
                            box = await img.bounding_box()
                            if box and (box['width'] > 200 or box['height'] > 200):
                                src = await img.get_attribute('src')
                                if src and 'logo' not in src.lower() and 'icon' not in src.lower():
                                    fotos_set.add(src)
                        except:
                            continue
                except:
                    pass
            
            fotos = list(fotos_set)[:10]
            
            produto = {
                'titulo': titulo,
                'marca': marca,
                'preco': preco,
                'descricao': descricao[:500] if descricao else '',
                'detalhes': detalhes[:20],
                'fotos': fotos,
                'url': url
            }
            
            print(f"✅ Produto extraído: {produto.get('titulo', 'Sem título')[:50]}")
            return produto
            
        except Exception as e:
            print(f"❌ Erro ao extrair produto: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def extrair_ofertas(self, url):
        """Extrair todas as ofertas de uma página de comparação"""
        try:
            print(f"🔍 Acessando página de ofertas: {url}")
            await self.page.goto(url, wait_until="domcontentloaded", timeout=20000)
            
            # Aguardar ofertas carregarem (reduzido de 8s para 3s)
            await asyncio.sleep(3)
            
            # Scroll rápido para carregar lazy loading
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1)  # Reduzido de 2s para 1s
            
            # Extrair título do produto
            titulo = await self.extrair_texto_seletor([
                'h1',
                '.product-title',
                'meta[property="og:title"]'
            ])
            print(f"  📝 Produto: {titulo}")
            
            # Extrair todas as ofertas usando o seletor correto
            ofertas = []
            elements = await self.page.query_selector_all('.promocao-produtos-item')
            print(f"  ✓ Encontrou {len(elements)} cards de ofertas")
            
            # Extrair dados de cada oferta
            for i, el in enumerate(elements[:100]):  # Limitar a 100 ofertas
                try:
                    # Extrair nome da loja (do atributo alt da imagem)
                    loja = ''
                    imagem_loja = ''
                    try:
                        loja_img = await el.query_selector('.store-image')
                        if loja_img:
                            loja = await loja_img.get_attribute('alt')
                            if not loja:
                                loja = await loja_img.get_attribute('title')
                            # Extrair URL da imagem da loja
                            imagem_loja = await loja_img.get_attribute('src')
                            if not imagem_loja or 'loading-images' in imagem_loja:
                                imagem_loja = await loja_img.get_attribute('data-src')
                    except:
                        pass
                    
                    # Extrair preço (em US$)
                    preco = ''
                    try:
                        preco_el = await el.query_selector('.promocao-item-preco-oferta strong')
                        if preco_el:
                            preco = await preco_el.inner_text()
                            preco = preco.strip()
                    except:
                        pass
                    
                    # Extrair link para o site da loja
                    link_loja = ''
                    try:
                        link_el = await el.query_selector('a.btn-store-redirect')
                        if link_el:
                            link_loja = await link_el.get_attribute('href')
                    except:
                        pass
                    
                    # Extrair nome do produto específico (variação)
                    nome_produto = ''
                    try:
                        nome_el = await el.query_selector('.promocao-item-nome a')
                        if nome_el:
                            nome_produto = await nome_el.inner_text()
                            nome_produto = nome_produto.strip()
                    except:
                        pass
                    
                    # Extrair link do produto (interno comprasparaguai)
                    link_produto = ''
                    try:
                        link_el = await el.query_selector('.promocao-item-nome a')
                        if link_el:
                            href = await link_el.get_attribute('href')
                            if href:
                                if href.startswith('http'):
                                    link_produto = href
                                else:
                                    link_produto = f"https://www.comprasparaguai.com.br{href}"
                    except:
                        pass
                    
                    # Extrair imagem do produto
                    imagem = ''
                    try:
                        img_el = await el.query_selector('.promocao-item-img img')
                        if img_el:
                            imagem = await img_el.get_attribute('src')
                            if not imagem or 'loading-images' in imagem:
                                imagem = await img_el.get_attribute('data-src')
                    except:
                        pass
                    
                    if loja or preco:
                        ofertas.append({
                            'loja': loja,
                            'imagem_loja': imagem_loja,
                            'preco': preco,
                            'link_loja': link_loja,
                            'link_produto': link_produto,
                            'produto': nome_produto,
                            'imagem': imagem
                        })
                        print(f"    • {loja}: {preco} - {nome_produto[:40]}")
                        if imagem_loja:
                            print(f"      🏪 Logo: {imagem_loja[:50]}...")
                        else:
                            print(f"      🏪 Sem logo")
                except Exception as e:
                    print(f"  ⚠️ Erro ao extrair oferta {i+1}: {e}")
                    continue
            
            resultado = {
                'titulo': titulo,
                'total_ofertas': len(ofertas),
                'ofertas': ofertas,
                'url': url
            }
            
            print(f"✅ {len(ofertas)} ofertas extraídas")
            return resultado
            
        except Exception as e:
            print(f"❌ Erro ao extrair ofertas: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def extrair_detalhes_produto(self, url):
        """Extrair detalhes completos de um produto do Compras Paraguai"""
        try:
            print(f"🔍 Extraindo detalhes do produto: {url}")
            # Usar domcontentloaded é mais rápido que networkidle
            await self.page.goto(url, wait_until="domcontentloaded", timeout=20000)
            
            # Aguardar apenas o necessário para o conteúdo principal carregar
            await asyncio.sleep(1)
            
            # Nome do produto
            nome = await self.extrair_texto_seletor([
                'h1.product-title',
                'h1',
                '.product-name'
            ])
            
            # Preço - buscar no campo "Por: US$ XXX"
            preco = None
            try:
                # Buscar na área de preço do produto
                price_divs = await self.page.query_selector_all('.header-product-info--price')
                for div in price_divs:
                    texto = await div.inner_text()
                    if 'Por:' in texto or 'US$' in texto:
                        # Extrair apenas o preço
                        lines = texto.split('\n')
                        for line in lines:
                            line = line.strip()
                            if line.startswith('US$') or line.startswith('R$'):
                                preco = line
                                break
                        if preco:
                            break
            except:
                pass
            
            # Se não encontrou, tentar no small "Preço atual:"
            if not preco:
                try:
                    small = await self.page.query_selector('small')
                    if small:
                        texto = await small.inner_text()
                        if 'Preço atual:' in texto:
                            preco = texto.replace('Preço atual:', '').strip()
                except:
                    pass
            
            if not preco or len(preco) < 3:
                preco = "Consultar"
            
            # Thumbnail do produto - buscar imagem na galeria principal
            thumbnail = None
            try:
                # Buscar link da galeria (fancybox) que tem a imagem grande
                gallery_link = await self.page.query_selector('a[data-fancybox-group="thumbHead"]')
                if gallery_link:
                    thumbnail = await gallery_link.get_attribute('href')
                
                # Se não encontrou, buscar a imagem dentro
                if not thumbnail:
                    img_in_gallery = await self.page.query_selector('.header-product-detail-image img, .product-detail-image img')
                    if img_in_gallery:
                        src = await img_in_gallery.get_attribute('src')
                        # Se for med, tentar trocar para big
                        if src and 'thumbs/med' in src:
                            thumbnail = src.replace('thumbs/med', 'thumbs/big')
                        else:
                            thumbnail = src
                
                # Última tentativa: procurar qualquer imagem grande do produto
                if not thumbnail:
                    all_imgs = await self.page.query_selector_all('img')
                    for img in all_imgs:
                        try:
                            alt = await img.get_attribute('alt') or ''
                            src = await img.get_attribute('src')
                            if not src:
                                src = await img.get_attribute('data-src')
                            
                            # Verificar se tem o nome do produto no alt e é uma imagem de produto
                            if src and 'fotos/produtos' in src and len(alt) > 10:
                                # Tentar pegar versão big
                                if 'thumbs/med' in src:
                                    thumbnail = src.replace('thumbs/med', 'thumbs/big')
                                else:
                                    thumbnail = src
                                break
                        except:
                            continue
            except:
                pass
            
            # Logo da loja - buscar link com href contendo "loja"
            logo_loja = None
            try:
                logo_elem = await self.page.query_selector('a[href*="loja"] img, a[href*="/l/"] img')
                if logo_elem:
                    logo_loja = await logo_elem.get_attribute('src')
                    if logo_loja and not logo_loja.startswith('http'):
                        # Se for caminho relativo, completar com domínio
                        logo_loja = f'https://www.comprasparaguai.com.br{logo_loja}'
            except:
                pass
            
            # Especificações Básicas - buscar na tabela "INFORMAÇÕES BÁSICAS"
            specs_basicas = []
            
            # Buscar tabela de informações básicas
            try:
                # Encontrar a tabela com INFORMAÇÕES BÁSICAS
                table = await self.page.query_selector('table.table-details, table.table-hover')
                if table:
                    rows = await table.query_selector_all('tbody tr')
                    for row in rows:
                        tds = await row.query_selector_all('td')
                        if len(tds) == 2:
                            label = await tds[0].inner_text()
                            value = await tds[1].inner_text()
                            label = label.strip()
                            value = value.strip()
                            if label and value:
                                specs_basicas.append(f"{label}: {value}")
            except:
                pass
            
            # Se não encontrou, tentar outras estruturas
            if len(specs_basicas) < 2:
                try:
                    rows = await self.page.query_selector_all('table tr')
                    for row in rows[:20]:
                        tds = await row.query_selector_all('td')
                        if len(tds) == 2:
                            label = await tds[0].inner_text()
                            value = await tds[1].inner_text()
                            label = label.strip()
                            value = value.strip()
                            if label and value and len(label) < 50:
                                specs_basicas.append(f"{label}: {value}")
                except:
                    pass
            
            # Especificações Extras - buscar em "Informações Extras" e descrições
            specs_extras = []
            
            # Buscar seção "Informações Extras" ou descrições (limite de 10 para ser mais rápido)
            try:
                # Procurar pela div block-paragraph que vem depois de "Informações Extras"
                info_sections = await self.page.query_selector_all('.block-paragraph, .product-description, [class*="descri"]')
                
                # Limitar a busca para não ficar lento
                for section in info_sections[:10]:
                    if len(specs_extras) >= 5:
                        break
                        
                    # Verificar se não está dentro do autocomplete ou mais buscados
                    parent_classes = await section.evaluate('el => el.closest(".autocomplete-most-searched, .autocomplete, #autocomplete") ? "skip" : ""')
                    if parent_classes == "skip":
                        continue
                    
                    texto = await section.inner_text()
                    texto = texto.strip()
                    # Pegar descrições com conteúdo útil
                    if texto and 50 < len(texto) < 1000:
                        # Evitar textos genéricos de navegação
                        if not any(x in texto.lower() for x in ['cookie', 'whatsapp', 'política', 'termos', 'login', 'cadastre-se', 'mais buscados']):
                            # Dividir em sentenças se for muito grande
                            if len(texto) > 300:
                                # Dividir por pontos
                                sentences = texto.split('.')
                                for sent in sentences[:3]:  # Limitar sentenças
                                    if len(specs_extras) >= 5:
                                        break
                                    sent = sent.strip()
                                    if sent and 20 < len(sent) < 300:
                                        specs_extras.append(sent + '.')
                            else:
                                specs_extras.append(texto)
            except:
                pass
            
            # Se não encontrou, buscar listas com características técnicas
            if len(specs_extras) < 2:
                try:
                    all_lists = await self.page.query_selector_all('ul li, ol li')
                    for li in all_lists[:50]:
                        # Verificar se não está dentro do autocomplete
                        parent_classes = await li.evaluate('el => el.closest(".autocomplete-most-searched, .autocomplete, #autocomplete") ? "skip" : ""')
                        if parent_classes == "skip":
                            continue
                            
                        texto = await li.inner_text()
                        texto = texto.strip()
                        # Pegar itens que parecem specs técnicas
                        if texto and 15 < len(texto) < 200:
                            # Palavras-chave técnicas
                            tech_words = ['processador', 'memória', 'armazenamento', 'gpu', 'resolução', 'fps', 
                                        'hdmi', 'usb', 'velocidade', 'compatível', 'ram', 'ssd', 'hdd', 'cpu',
                                        'cores', 'threads', 'ghz', 'tb', 'gb', 'ray tracing', '4k', '8k', 'wifi',
                                        'bluetooth', 'ethernet', 'dolby', 'atmos', 'hdr']
                            if any(word in texto.lower() for word in tech_words):
                                specs_extras.append(texto)
                                if len(specs_extras) >= 10:
                                    break
                except:
                    pass
            
            resultado = {
                'nome': nome or 'Produto',
                'preco': preco or 'Consultar',
                'thumbnail': thumbnail,
                'logo_loja': logo_loja,
                'especificacoes_basicas': specs_basicas,
                'especificacoes_extras': specs_extras,
                'url': url
            }
            
            print(f"✅ Detalhes extraídos: {nome}")
            print(f"   💰 Preço: {preco}")
            print(f"   🖼️  Thumbnail: {thumbnail[:50] if thumbnail else 'Não encontrado'}...")
            print(f"   🏪 Logo loja: {logo_loja[:50] if logo_loja else 'Não encontrado'}...")
            print(f"   📋 Specs básicas: {len(specs_basicas)} itens")
            print(f"   ⚙️  Specs extras: {len(specs_extras)} itens")
            return resultado
            
        except Exception as e:
            print(f"❌ Erro ao extrair detalhes: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def fechar(self):
        """Fechar o navegador"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


# Instância global
extractor = None

@app.route('/')
def index():
    return render_template('extrator.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    """Rota para buscar produtos"""
    try:
        data = request.get_json()
        produto = data.get('produto', '').strip()
        
        if not produto:
            return jsonify({'success': False, 'error': 'Produto não informado'})
        
        # Criar URL de busca do Compras Paraguai
        produto_encoded = produto.replace(' ', '-').lower()
        url = f"https://www.comprasparaguai.com.br/{produto_encoded}"
        
        # Extrair ofertas
        async def extrair():
            extractor = ProductExtractor()
            return await extractor.extrair_ofertas(url)
        
        resultado = run_async(extrair())
        
        if resultado and 'ofertas' in resultado:
            # Salvar na sessão
            session['ofertas'] = resultado['ofertas']
            session['produto'] = produto
            
            return jsonify({
                'success': True, 
                'total': len(resultado['ofertas'])
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'Nenhuma oferta encontrada'
            })
            
    except Exception as e:
        print(f"Erro ao buscar: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/ofertas')
def ofertas():
    """Página de ofertas"""
    return render_template('ofertas.html')

@app.route('/api/ofertas', methods=['GET'])
def api_ofertas():
    """Retorna ofertas da sessão"""
    ofertas = session.get('ofertas', [])
    return jsonify({'ofertas': ofertas})

@app.route('/extrator')
def extrator():
    """Página antiga de extrator direto"""
    return render_template('extrator.html')

@app.route('/detalhes', methods=['GET', 'POST'])
def detalhes():
    if request.method == 'POST':
        # Receber dados via POST e armazenar temporariamente
        data = request.get_json() if request.is_json else request.form
        url = data.get('url', '')
        logo = data.get('logo', '')
        
        print(f"📥 POST /detalhes recebido:")
        print(f"   URL: {url[:80] if url else 'Nenhuma'}...")
        print(f"   Logo: {logo[:80] if logo else 'Nenhuma'}...")
        
        # Gerar ID único para esta sessão
        detail_id = secrets.token_urlsafe(16)
        detalhes_temp[detail_id] = {'url': url, 'logo': logo}
        
        print(f"   💾 Armazenado com ID: {detail_id}")
        print(f"   📊 Total no cache: {len(detalhes_temp)} itens")
        
        return jsonify({'success': True, 'detail_id': detail_id})
    else:
        # GET - renderizar página
        return render_template('detalhes.html')

@app.route('/api/extrair', methods=['POST'])
def api_extrair():
    """Endpoint para extrair informações de um produto"""
    global extractor
    
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({"success": False, "error": "URL não fornecida"})
    
    if not url.startswith('http'):
        return jsonify({"success": False, "error": "URL inválida. Deve começar com http:// ou https://"})
    
    try:
        # Inicializar extractor se necessário
        if extractor is None:
            extractor = ProductExtractor()
            run_async(extractor.iniciar())
        
        # Detectar se é página de comprasparaguai
        if 'comprasparaguai.com.br' in url:
            # Verificar se é página de ofertas (sem __) ou detalhes (com __)
            if '__' in url:
                # É página de detalhes - redirecionar para a página de detalhes
                return jsonify({
                    "success": True,
                    "tipo": "redirect_detalhes",
                    "url": url
                })
            else:
                # É página de ofertas - extrair lista
                resultado = run_async(extractor.extrair_ofertas(url))
                
                if resultado:
                    return jsonify({
                        "success": True,
                        "tipo": "ofertas",
                        "produto": resultado
                    })
                else:
                    return jsonify({
                        "success": False,
                        "error": "Não foi possível extrair ofertas"
                    })
        else:
            # Extrair produto único
            produto = run_async(extractor.extrair_produto(url))
            
            if produto:
                return jsonify({
                    "success": True,
                    "tipo": "produto",
                    "produto": produto
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Não foi possível extrair informações do produto"
                })
            
    except Exception as e:
        print(f"❌ Erro na API: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/detalhes', methods=['POST'])
def api_detalhes():
    """Endpoint para extrair detalhes completos de um produto"""
    global extractor
    
    data = request.json
    detail_id = data.get('detail_id', '')
    url = data.get('url', '')
    logo_loja = None
    
    # Se veio detail_id, buscar da memória temporária
    if detail_id and detail_id in detalhes_temp:
        stored_data = detalhes_temp[detail_id]
        url = stored_data.get('url', '')
        logo_loja = stored_data.get('logo', '')
        print(f"📦 Recuperado do cache - URL: {url[:50]}...")
        print(f"📦 Logo da loja: {logo_loja[:50] if logo_loja else 'Nenhuma'}...")
        # Limpar da memória após usar
        del detalhes_temp[detail_id]
    
    if not url:
        return jsonify({"success": False, "error": "URL não fornecida"})
    
    if not url.startswith('http'):
        return jsonify({"success": False, "error": "URL inválida"})
    
    try:
        # Inicializar extractor se necessário
        if extractor is None:
            extractor = ProductExtractor()
            run_async(extractor.iniciar())
        
        # Extrair detalhes do produto
        detalhes = run_async(extractor.extrair_detalhes_produto(url))
        
        if detalhes:
            # Adicionar logo da loja se veio do armazenamento temporário
            if logo_loja:
                detalhes['logo_loja'] = logo_loja
            
            # Calcular markup e conversão de moeda
            preco_str = detalhes.get('preco', '')
            if preco_str:
                try:
                    # Extrair valor numérico do preço
                    # Exemplos: "US$ 100,00" -> 100.00 ou "US$ 1.139,00" -> 1139.00
                    import re
                    # Remove tudo exceto dígitos, vírgulas e pontos
                    preco_limpo = re.sub(r'[^\d,.]', '', preco_str)
                    
                    # Se tem vírgula e ponto, assumir formato brasileiro (1.139,00)
                    if ',' in preco_limpo and '.' in preco_limpo:
                        # Remover pontos (separador de milhares) e trocar vírgula por ponto
                        preco_limpo = preco_limpo.replace('.', '').replace(',', '.')
                    # Se tem apenas vírgula, assumir vírgula como decimal
                    elif ',' in preco_limpo:
                        preco_limpo = preco_limpo.replace(',', '.')
                    # Se tem apenas ponto, assumir ponto como decimal
                    
                    preco_dolar = float(preco_limpo)
                    
                    # Obter cotação do dólar
                    cotacao_dolar = obter_cotacao_dolar()
                    
                    # Calcular valores
                    preco_reais = preco_dolar * cotacao_dolar
                    taxa_bestguai = preco_reais * 0.27  # 27%
                    valor_total = preco_reais + taxa_bestguai
                    
                    # Adicionar cálculos ao response
                    detalhes['calculos'] = {
                        'preco_dolar': preco_dolar,
                        'cotacao_dolar': cotacao_dolar,
                        'preco_reais': preco_reais,
                        'taxa_bestguai': taxa_bestguai,
                        'valor_total': valor_total
                    }
                except Exception as e:
                    print(f"⚠️ Erro ao calcular markup: {e}")
            
            return jsonify({
                "success": True,
                "produto": detalhes
            })
        else:
            return jsonify({
                "success": False,
                "error": "Não foi possível extrair detalhes"
            })
            
    except Exception as e:
        print(f"❌ Erro na API detalhes: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Extrator de Produtos iniciando...")
    print("=" * 70)
    print("\n📱 Acesse: http://localhost:5000")
    print("\n💡 Cole um link de produto e extraia as informações!")
    print("\n⚠️  Pressione Ctrl+C para parar o servidor")
    print("=" * 70)
    
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
