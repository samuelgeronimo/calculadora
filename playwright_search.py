"""
Script para automação de busca no site comprasparaguai.com.br usando Playwright
Este script navega até o site, pesquisa por produtos e extrai opções de filtros
"""

import asyncio
from playwright.async_api import async_playwright
import json


async def search_and_get_filters(search_term: str = "ps5"):
    """
    Navega até comprasparaguai.com.br, pesquisa por um termo e extrai filtros disponíveis
    
    Args:
        search_term: Termo de busca (padrão: 'ps5')
    """
    async with async_playwright() as p:
        # Iniciar o navegador
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        try:
            print(f"🌐 Navegando para comprasparaguai.com.br...")
            await page.goto("https://www.comprasparaguai.com.br", timeout=60000)
            await page.wait_for_load_state("networkidle")
            
            print(f"🔍 Procurando campo de busca...")
            # Tentar diferentes seletores comuns para campos de busca
            search_selectors = [
                'input[type="search"]',
                'input[name="q"]',
                'input[name="search"]',
                'input[placeholder*="Buscar"]',
                'input[placeholder*="buscar"]',
                'input[placeholder*="Pesquisar"]',
                'input[placeholder*="pesquisar"]',
                '#search',
                '.search-input',
                '[aria-label*="search" i]',
                '[aria-label*="busca" i]'
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    search_input = await page.wait_for_selector(selector, timeout=3000)
                    if search_input:
                        print(f"✅ Campo de busca encontrado: {selector}")
                        break
                except:
                    continue
            
            if not search_input:
                # Se não encontrar, tentar procurar visualmente
                print("⚠️ Campo de busca não encontrado com seletores comuns")
                print("📸 Tirando screenshot para análise...")
                await page.screenshot(path="c:\\dev\\calculadora\\screenshot_inicial.png")
                return
            
            print(f"⌨️ Digitando '{search_term}'...")
            await search_input.fill(search_term)
            
            # Pressionar Enter ou procurar botão de busca
            print(f"🚀 Executando busca...")
            await search_input.press("Enter")
            
            # Aguardar resultados carregarem
            await page.wait_for_load_state("networkidle", timeout=30000)
            await asyncio.sleep(2)
            
            print(f"📸 Capturando página de resultados...")
            await page.screenshot(path="c:\\dev\\calculadora\\screenshot_resultados.png")
            
            print(f"📜 Rolando a página para encontrar filtros...")
            # Rolar a página gradualmente
            for i in range(5):
                await page.evaluate(f"window.scrollBy(0, {300 * (i + 1)})")
                await asyncio.sleep(0.5)
            
            await page.screenshot(path="c:\\dev\\calculadora\\screenshot_com_scroll.png")
            
            print(f"🔎 Procurando elementos de filtros...")
            # Procurar por elementos de filtro comuns
            filter_data = {
                "filtros_encontrados": [],
                "html_filtros": ""
            }
            
            # Seletores comuns para áreas de filtros
            filter_area_selectors = [
                '.filters',
                '.filter-panel',
                '.sidebar-filters',
                '[class*="filter"]',
                '[class*="filtro"]',
                'aside',
                '.sidebar',
                '[role="complementary"]'
            ]
            
            for selector in filter_area_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"✅ Área de filtros encontrada: {selector}")
                        for element in elements:
                            text = await element.inner_text()
                            html = await element.inner_html()
                            if len(text) > 50:  # Filtros geralmente têm bastante texto
                                filter_data["filtros_encontrados"].append({
                                    "selector": selector,
                                    "texto": text[:500],  # Primeiros 500 caracteres
                                    "html_preview": html[:1000]
                                })
                except Exception as e:
                    continue
            
            # Procurar por checkboxes, radios e selects (elementos típicos de filtro)
            print(f"🎛️ Procurando por controles de filtro específicos...")
            
            # Checkboxes
            checkboxes = await page.query_selector_all('input[type="checkbox"]')
            if checkboxes:
                print(f"✅ Encontrados {len(checkboxes)} checkboxes")
                checkbox_data = []
                for cb in checkboxes[:20]:  # Limitar a 20 para não sobrecarregar
                    try:
                        label = await cb.evaluate("""el => {
                            const label = el.closest('label') || document.querySelector(`label[for="${el.id}"]`);
                            return label ? label.innerText : el.getAttribute('name') || el.getAttribute('value') || 'sem label';
                        }""")
                        checkbox_data.append(label)
                    except:
                        pass
                filter_data["checkboxes"] = checkbox_data
            
            # Selects/dropdowns
            selects = await page.query_selector_all('select')
            if selects:
                print(f"✅ Encontrados {len(selects)} dropdowns")
                select_data = []
                for select in selects:
                    try:
                        options = await select.evaluate("""el => {
                            return Array.from(el.options).map(opt => opt.text);
                        }""")
                        select_data.append({
                            "opcoes": options
                        })
                    except:
                        pass
                filter_data["selects"] = select_data
            
            # Salvar dados coletados
            with open("c:\\dev\\calculadora\\filtros_extraidos.json", "w", encoding="utf-8") as f:
                json.dump(filter_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ Dados coletados e salvos!")
            print(f"📁 Screenshots salvos em: c:\\dev\\calculadora\\")
            print(f"📄 Dados dos filtros salvos em: filtros_extraidos.json")
            
            # Exibir resumo
            print(f"\n📊 RESUMO DOS FILTROS ENCONTRADOS:")
            print(f"   - Áreas de filtros: {len(filter_data.get('filtros_encontrados', []))}")
            print(f"   - Checkboxes: {len(filter_data.get('checkboxes', []))}")
            print(f"   - Dropdowns: {len(filter_data.get('selects', []))}")
            
            if filter_data.get('checkboxes'):
                print(f"\n🔘 OPÇÕES DE FILTROS (Checkboxes):")
                for i, checkbox in enumerate(filter_data['checkboxes'][:15], 1):
                    print(f"   {i}. {checkbox}")
            
            if filter_data.get('selects'):
                print(f"\n📋 OPÇÕES DE FILTROS (Dropdowns):")
                for i, select in enumerate(filter_data['selects'], 1):
                    print(f"   Dropdown {i}: {', '.join(select['opcoes'][:10])}")
            
            # Manter navegador aberto por alguns segundos
            print(f"\n⏳ Mantendo navegador aberto por 10 segundos para visualização...")
            await asyncio.sleep(10)
            
        except Exception as e:
            print(f"❌ Erro durante a execução: {str(e)}")
            await page.screenshot(path="c:\\dev\\calculadora\\screenshot_erro.png")
            raise
        finally:
            await browser.close()
            print(f"🔚 Navegador fechado.")


async def apply_filters(filter_selections: dict):
    """
    Aplica filtros selecionados para refinar a busca
    
    Args:
        filter_selections: Dicionário com os filtros a aplicar
    """
    # Esta função será implementada após identificarmos os filtros disponíveis
    print("Função de aplicar filtros será implementada após análise dos filtros encontrados")


if __name__ == "__main__":
    print("🚀 Iniciando automação de busca no comprasparaguai.com.br")
    print("=" * 60)
    asyncio.run(search_and_get_filters("ps5"))
