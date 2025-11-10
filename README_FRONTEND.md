# 🌐 Frontend Web - Buscador Compras Paraguai

## 📋 Descrição

Interface web completa para buscar produtos no site comprasparaguai.com.br com sistema de filtros interativos.

## ✨ Funcionalidades

### 1️⃣ Busca de Produtos
- Digite o termo de busca (ex: ps5, notebook, iphone)
- Sistema automático de extração de filtros
- Contador de produtos encontrados

### 2️⃣ Filtros Dinâmicos
- **🏪 Lojas:** Selecione múltiplas lojas
- **🏷️ Marcas:** Filtre por marcas específicas
- **📊 Ordenação:** Menor preço, maior preço, mais novos, etc.

### 3️⃣ Recursos Interativos
- Busca dentro dos filtros (search box)
- Selecionar todos / Limpar seleção
- Visualização de filtros selecionados
- Aplicação em tempo real

### 4️⃣ Resultados
- Grade de produtos com imagens
- Preços destacados
- Link direto para o produto
- Informações da loja

## 🚀 Como Executar

### 1. Instalar dependências
```powershell
pip install flask playwright
```

### 2. Iniciar o servidor
```powershell
python app.py
```

### 3. Acessar a interface
```
http://localhost:5000
```

## 📖 Fluxo de Uso

1. **Digite o termo de busca** (ex: "ps5")
2. **Clique em "Buscar"**
3. **Aguarde a extração dos filtros** (15-30 segundos)
4. **Selecione os filtros desejados:**
   - Lojas (múltipla seleção)
   - Marcas (múltipla seleção)
   - Ordenação (única seleção)
5. **Clique em "Aplicar Filtros"**
6. **Visualize os produtos encontrados**

## 🎯 Endpoints da API

### POST /api/buscar
Realiza busca e retorna filtros disponíveis

**Request:**
```json
{
  "termo": "ps5"
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "abc123",
  "termo": "ps5",
  "filtros": {
    "lojas": [...],
    "marcas": [...],
    "ordenacao": [...],
    "total_produtos": 104
  }
}
```

### POST /api/aplicar-filtros
Aplica filtros selecionados

**Request:**
```json
{
  "session_id": "abc123",
  "filtros": {
    "lojas": ["filtro-Atacado Connect"],
    "marcas": ["filtro-Sony"],
    "ordenacao": "Menor Preço"
  }
}
```

**Response:**
```json
{
  "success": true,
  "resultados": {
    "aplicados": [...],
    "erros": [...]
  },
  "produtos": [...]
}
```

### POST /api/limpar-sessao
Encerra sessão do navegador

**Request:**
```json
{
  "session_id": "abc123"
}
```

## 🎨 Tecnologias Utilizadas

- **Backend:** Flask (Python)
- **Automação:** Playwright
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Estilo:** CSS Grid, Flexbox, Animações

## 📱 Responsivo

A interface é totalmente responsiva e funciona em:
- 💻 Desktop
- 📱 Tablet
- 📱 Mobile

## ⚡ Performance

- Filtros em cache durante a sessão
- Loading states para feedback visual
- Timeout configurado para evitar travamentos
- Máximo de 15 produtos retornados por vez

## 🔧 Configurações

### Timeout do navegador
```python
self.page.set_default_timeout(90000)  # 90 segundos
```

### Modo headless
```python
self.browser = await self.playwright.chromium.launch(headless=True)
```

## 🐛 Troubleshooting

### Erro de timeout
- Aumente o timeout em `app.py`
- Verifique sua conexão com a internet

### Filtros não aparecem
- Execute a busca novamente
- Verifique se o site está acessível

### Sessão expirada
- Realize uma nova busca
- Não feche o navegador durante o processo

## 💡 Dicas de Uso

1. **Para melhores ofertas:**
   - Selecione marca "Sony"
   - Ordenação: "Menor Preço"

2. **Para produtos novos:**
   - Ordenação: "Mais Novos"

3. **Para lojas específicas:**
   - Selecione 2-3 lojas confiáveis
   - Compare preços

4. **Use o campo de busca:**
   - Filtre lojas digitando no campo de busca
   - Filtre marcas rapidamente

## 📂 Estrutura de Arquivos

```
calculadora/
├── app.py                 # Servidor Flask
├── templates/
│   └── index.html        # Interface web
├── static/
│   └── style.css         # Estilos CSS
├── requirements.txt      # Dependências
└── README_FRONTEND.md    # Esta documentação
```

## 🔐 Segurança

- Session IDs gerados com `secrets.token_hex()`
- Validação de dados no backend
- Sanitização de inputs
- CORS configurado (se necessário)

## 🚀 Melhorias Futuras

- [ ] Salvar buscas favoritas
- [ ] Histórico de buscas
- [ ] Comparador de preços
- [ ] Alertas de preço
- [ ] Exportar resultados (CSV/JSON)
- [ ] Filtro por faixa de preço
- [ ] Filtro por categoria

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs do servidor
2. Veja os screenshots gerados
3. Consulte a documentação do Playwright

---

**Desenvolvido com ❤️ usando Flask + Playwright**
