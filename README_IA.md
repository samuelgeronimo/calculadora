# 🤖 Sistema de Comparação de Preços com IA

Sistema inteligente de comparação de preços que usa **GPT-4 Vision** para analisar marketplaces brasileiros e encontrar os melhores preços.

## 🚀 Configuração Rápida

### 1️⃣ Instalar Dependências

```bash
pip install openai pillow playwright flask
playwright install chromium
```

### 2️⃣ Configurar API OpenAI

**Opção A - Script Interativo (Recomendado):**
```bash
python config_api.py
```

**Opção B - Manual:**
```powershell
# PowerShell (Windows)
$env:OPENAI_API_KEY = "sk-sua-chave-aqui"
$env:USE_AI_AGENT = "true"
```

### 3️⃣ Executar

```bash
python run_with_env.py
```

Ou diretamente:
```bash
python app.py
```

## 🤖 Como Funciona

### Modo IA (Recomendado)

1. **Screenshot**: Tira screenshot da página de resultados
2. **Análise Visual**: GPT-4 Vision analisa a imagem
3. **Extração Inteligente**: Identifica produtos exatos
4. **Validação**: Filtra apenas produtos correspondentes
5. **Tabela Comparativa**: Exibe menor preço de cada marketplace

**Vantagens:**
- ✅ Não depende de seletores CSS (sites mudam constantemente)
- ✅ Identifica produtos semanticamente
- ✅ Adapta-se automaticamente a mudanças
- ✅ Mais preciso que regex/seletores

### Modo Tradicional

Usa seletores CSS configurados manualmente (menos confiável).

## 📊 Marketplaces Suportados

- ✅ Mercado Livre
- ✅ Amazon Brasil
- ✅ Shopee
- ✅ Americanas
- ✅ Magazine Luiza
- ✅ Casas Bahia
- ✅ KaBuM!
- ✅ Loja do Mecânico

## 💡 Uso

1. Acesse: `http://localhost:5000`
2. Cole link de um produto
3. Clique em "Buscar Melhores Preços"
4. Veja tabela comparativa instantânea

## ⚙️ Configurações

### Variáveis de Ambiente

```env
OPENAI_API_KEY=sk-...          # Obrigatória para modo IA
USE_AI_AGENT=true              # true=IA, false=Tradicional
```

### Custo Estimado

- **GPT-4o-mini**: ~$0.01-0.02 por comparação (8 marketplaces)
- Screenshot em baixa resolução para otimizar custo
- Timeout de 90s para garantir resposta rápida

## 🔧 Troubleshooting

### "OPENAI_API_KEY não configurada"
```bash
python config_api.py
```

### Erro de timeout
- Aumente timeout em `app.py` (linha: `timeout=90`)
- Ou reduza número de marketplaces

### IA retorna produtos errados
- Produto pode não existir no marketplace
- Tente nome mais específico
- Verifique se marketplace tem o produto

## 📝 Exemplo de Resposta

```json
{
  "success": true,
  "comparacao": {
    "mercadolivre": {
      "nome": "Mercado Livre",
      "produtos": [
        {
          "titulo": "iPhone 15 Pro Max 256GB",
          "preco": 7899.00,
          "link": "https://..."
        }
      ]
    }
  }
}
```

## 🎯 Próximas Melhorias

- [ ] Cache de resultados (evitar buscas duplicadas)
- [ ] Histórico de preços
- [ ] Alertas de queda de preço
- [ ] Exportar para Excel/PDF
- [ ] API pública

## 📄 Licença

MIT
