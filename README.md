# 🛒 Sistema de Extração e Comparação de Produtos

Sistema web completo para extração de produtos do site comprasparaguai.com.br com calculadora de preços automática incluindo cotação do dólar em tempo real e markup.

## 🚀 Como Iniciar

### Método 1: Script de Produção (Recomendado)
```cmd
iniciar.bat
```

### Método 2: Terminal
```powershell
python app.py
```

O servidor iniciará em `http://localhost:5000`

## ✨ Funcionalidades

### Extração de Produtos
- ✅ Busca e extração automática de ofertas do comprasparaguai.com.br
- ✅ Extração completa de detalhes do produto
- ✅ Miniaturas de imagens
- ✅ Logo da loja extraído automaticamente
- ✅ Especificações técnicas organizadas em categorias

### Calculadora de Preços 💰
Exibe automaticamente na página de detalhes:
- **Preço em Dólar**: Preço original do produto
- **Valor do Dólar**: Cotação em tempo real via AwesomeAPI + R$ 0,10
- **Valor em Reais**: Conversão automática (USD × Cotação)
- **Taxa Bestguai**: Markup de 27% sobre o preço em reais
- **Valor Total**: Preço final incluindo markup

Exemplo:
```
Produto: iPhone 15 Pro Max
Preço original: US$ 1.139,00
Cotação do dólar: R$ 5,41 (API: R$ 5,31 + R$ 0,10)
Valor em Reais: R$ 6.161,99
Taxa Bestguai (27%): R$ 1.663,74
Valor Total: R$ 7.825,73
```

### Interface e Navegação
- ✅ Comparação visual de ofertas
- ✅ Ordenação por preço, loja, frete
- ✅ URLs limpos com POST + sessionStorage
- ✅ Navegação com memória (cache de ofertas ao retornar)
- ✅ Interface responsiva e moderna

## 🔧 Tecnologias

- **Backend**: Python 3.12 + Flask 3.0.0
- **Web Scraping**: Playwright (async_api)
- **API Cotação**: AwesomeAPI (economia.awesomeapi.com.br/json/last/USD-BRL)
- **HTTP Client**: requests 2.31.0
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)

## ⚡ Performance

- Tempo de extração de ofertas: ~8-12 segundos
- Tempo de detalhes do produto: ~3-5 segundos
- Cotação do dólar: ~1 segundo (com cache)
- Cálculos automáticos em tempo real

## 📦 Instalação

### 1. Instalar dependências
```powershell
pip install -r requirements.txt
```

### 2. Instalar navegadores do Playwright
```powershell
playwright install chromium
```

## ⚙️ Configuração

### Alterar Porta do Servidor
Em `app.py`, linha 842:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Ajustar Percentual de Markup
Em `app.py`, linha 787:
```python
taxa_bestguai = preco_reais * 0.27  # Altere 0.27 para o percentual desejado
```

### Modificar Ajuste na Cotação do Dólar
Em `app.py`, linha 20:
```python
cotacao_final = cotacao_base + 0.10  # Altere 0.10 para o valor desejado
```

## 📁 Estrutura de Arquivos

```
calculadora/
├── app.py                 # Servidor Flask e lógica de extração
├── requirements.txt       # Dependências Python
├── iniciar.bat           # Script de inicialização (Windows)
├── README.md             # Documentação
└── templates/
    ├── index.html        # Página de busca
    ├── ofertas.html      # Lista de ofertas
    └── detalhes.html     # Detalhes + calculadora
```

## 🐛 Solução de Problemas

### Erro: "Could not convert string to float"
- O sistema já trata formatos US$ 100,00 e US$ 1.139,00 automaticamente
- Se persistir, verifique o formato do preço no HTML da origem

### API de Cotação Offline
- Cotação padrão (fallback): R$ 5,60
- Timeout da API: 5 segundos
- Verifique sua conexão com internet

### Porta 5000 em Uso
```powershell
# Matar processos Python existentes
taskkill /F /IM python.exe
```

## 📊 Uso do Sistema

1. **Buscar Produto**: Digite na página inicial (ex: "ps5")
2. **Ver Ofertas**: Clique em "Ver Ofertas" para comparar
3. **Ver Detalhes**: Clique em qualquer oferta
4. **Calculadora**: Visualize automaticamente preços convertidos e markup
5. **Voltar**: Navegue sem recarregar dados (memória de ofertas)
