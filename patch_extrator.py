import re

# Ler o arquivo
with open('templates/extrator.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar CSS antes de </style>
css_to_add = '''        
        /* Estilos para sugestões de categorias */
        .sugestoes-container {
            background: #f8f9fa;
            padding: 20px;
            margin: 20px 0;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        
        .sugestoes-title {
            font-size: 14px;
            font-weight: 700;
            color: #667eea;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }
        
        .sugestoes-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .sugestao-tag {
            background: white;
            border: 2px solid #e2e8f0;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            color: #333;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
            display: inline-block;
        }
        
        .sugestao-tag:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }
'''

content = content.replace('    </style>', css_to_add + '    </style>')

# 2. Adicionar seção de sugestões antes de <div class="ofertas-lista">
sugestoes_html = '''                        ${data.sugestoes && data.sugestoes.length > 0 ? `
                        <div class="sugestoes-container">
                            <div class="sugestoes-title">📂 Sugestões de Categorias</div>
                            <div class="sugestoes-list">
                                ${data.sugestoes.map(sug => `
                                    <a href="${sug.link}" class="sugestao-tag" target="_blank">
                                        ${sug.nome}
                                    </a>
                                `).join('')}
                            </div>
                        </div>
                        ` : ''}
                        '''

content = content.replace(
    '                    <div class="produto-content">\r\n                        <div class="ofertas-lista">',
    '                    <div class="produto-content">\r\n' + sugestoes_html + '<div class="ofertas-lista">'
)

# Salvar o arquivo
with open('templates/extrator.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Arquivo atualizado com sucesso!")
