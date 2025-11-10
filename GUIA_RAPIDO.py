"""
🎯 GUIA RÁPIDO - Como Usar os Scripts de Automação
"""

print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    🎮 GUIA RÁPIDO DE USO                            ║
║              Automação de Busca - Compras Paraguai                   ║
╚══════════════════════════════════════════════════════════════════════╝

📋 OPÇÕES DISPONÍVEIS:

1️⃣  EXTRAÇÃO INICIAL DE FILTROS
   Comando: python playwright_search.py
   
   O que faz:
   ✅ Navega até comprasparaguai.com.br
   ✅ Pesquisa por 'ps5'
   ✅ Rola a página para encontrar filtros
   ✅ Extrai TODOS os filtros disponíveis
   ✅ Salva dados em filtros_extraidos.json
   ✅ Gera screenshots automáticos
   
   Quando usar: Primeira execução ou quando quiser atualizar filtros

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣  DEMONSTRAÇÃO VISUAL INTERATIVA
   Comando: python demo_visual.py
   
   O que faz:
   ✅ Abre navegador em modo visual
   ✅ Realiza busca por 'ps5'
   ✅ Aplica ordenação por "Menor Preço"
   ✅ Destaca área de filtros na página
   ✅ Mantém navegador aberto por 60s para interação manual
   ✅ Mostra 104 produtos encontrados
   
   Quando usar: Para ver os filtros em ação e testar manualmente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3️⃣  AUTOMAÇÃO PERSONALIZADA (Requer edição)
   Arquivo: busca_interativa.py
   
   Como usar:
   1. Abra o arquivo busca_interativa.py
   2. Vá até a função busca_interativa()
   3. Modifique os filtros que deseja aplicar:
   
   Exemplo:
   ```python
   # Filtrar por marca Sony
   await busca.aplicar_filtro_marca("Sony")
   
   # Filtrar por loja específica
   await busca.aplicar_filtro_loja("Atacado Connect")
   
   # Ordenar por menor preço
   await busca.ordenar_por("Menor Preço")
   ```
   
   4. Execute: python busca_interativa.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 FILTROS DISPONÍVEIS EXTRAÍDOS:

🏪 LOJAS (20+ opções):
   • Atacado Connect      • Mobile Zone         • Mega Eletro
   • Cellshop            • New Zone            • Raio Laser
   • Star Games          • Atlantico Shop      • Visãovip
   • Shopping China      • Super Games         • E muito mais...
   • Nissei              • Atacado Collections

🏷️  MARCAS (principais):
   • Sony      • Logitech    • JBL
   • Nacon     • Kingston    • SteelSeries
   • Razer     • Redragon

📊 ORDENAÇÃO:
   1. Relevância
   2. Menor Preço ⭐ (Recomendado para melhores ofertas)
   3. Maior Preço
   4. Produto (A-Z)
   5. Produto (Z-A)
   6. Mais Novos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 EXEMPLOS DE USO AVANÇADO:

1. Buscar PS5 da Sony por menor preço:
   ```python
   await busca.buscar_produto("ps5")
   await busca.aplicar_filtro_marca("Sony")
   await busca.ordenar_por("Menor Preço")
   ```

2. Buscar em loja específica:
   ```python
   await busca.buscar_produto("ps5")
   await busca.aplicar_filtro_loja("Atacado Connect")
   await busca.ordenar_por("Menor Preço")
   ```

3. Combinar múltiplos filtros:
   ```python
   await busca.buscar_produto("ps5")
   await busca.aplicar_filtro_marca("Sony")
   await busca.aplicar_filtro_loja("Cellshop")
   await busca.ordenar_por("Mais Novos")
   await busca.capturar_resultados()
   ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 ARQUIVOS GERADOS:

✅ filtros_extraidos.json       - Todos os filtros em formato JSON
✅ demo_visual_filtros.png      - Screenshot da página com filtros
✅ screenshot_resultados.png    - Screenshot dos resultados de busca
✅ screenshot_com_scroll.png    - Screenshot após rolar página
✅ resultados_filtrados.png     - Screenshot com filtros aplicados

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 SEQUÊNCIA RECOMENDADA PARA INICIANTES:

1. python demo_visual.py
   ↓
   Entenda como funciona e veja os filtros destacados
   
2. Analise filtros_extraidos.json
   ↓
   Veja todas as opções de filtros disponíveis
   
3. Edite busca_interativa.py
   ↓
   Personalize os filtros que deseja aplicar
   
4. python busca_interativa.py
   ↓
   Execute sua busca personalizada

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ DICAS PRO:

• O navegador fica aberto para você interagir manualmente
• Screenshots são salvos automaticamente
• Filtros podem ser combinados para refinar ainda mais
• Use "Menor Preço" para encontrar melhores ofertas
• Marque Sony para produtos originais do PS5
• Combine loja + marca + ordenação para busca perfeita

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ PRECISA DE AJUDA?

1. Leia RESUMO_PROJETO.md para documentação completa
2. Veja README.md para instruções de instalação
3. Os scripts têm comentários explicativos em português

╔══════════════════════════════════════════════════════════════════════╗
║                     ✨ BOA BUSCA! ✨                                ║
╚══════════════════════════════════════════════════════════════════════╝
""")
