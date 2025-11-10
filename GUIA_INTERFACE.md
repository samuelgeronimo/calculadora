# 🎯 GUIA RÁPIDO - Frontend Web

## ✅ Servidor Flask Rodando!

**URL:** http://localhost:5000

---

## 📖 Como Usar a Interface

### Passo 1: Buscar Produto
1. Digite o produto no campo de busca (ex: "ps5")
2. Clique em **"Buscar"**
3. Aguarde 15-30 segundos para extração dos filtros

### Passo 2: Visualizar Filtros
Após a busca, você verá:
- 🏪 **Lojas disponíveis** (37+ opções)
- 🏷️ **Marcas disponíveis** (32+ opções)
- 📊 **Opções de ordenação** (6 opções)

### Passo 3: Selecionar Filtros

**Filtrar Lojas:**
- Use o campo de busca para encontrar lojas
- Clique nos checkboxes para selecionar
- Use "Selecionar Todos" ou "Limpar"

**Filtrar Marcas:**
- Use o campo de busca para encontrar marcas
- Clique nos checkboxes para selecionar
- Combine múltiplas marcas

**Ordenação:**
- Selecione no dropdown
- **Menor Preço** → Melhores ofertas
- **Mais Novos** → Lançamentos
- **Relevância** → Mais pertinentes

### Passo 4: Aplicar Filtros
1. Revise os filtros selecionados (aparecem com tags coloridas)
2. Clique em **"✅ Aplicar Filtros"**
3. Aguarde 10-20 segundos
4. Veja os produtos filtrados!

### Passo 5: Ver Produtos
- Grade com imagens dos produtos
- Preços em destaque
- Nome da loja
- Botão "Ver Produto" (abre em nova aba)

---

## 🎨 Funcionalidades da Interface

### 🔍 Busca Inteligente
- Campo de busca em cada seção de filtros
- Filtragem em tempo real
- Não afeta os checkboxes selecionados

### 📌 Filtros Selecionados
- Visualização com tags coloridas:
  - 🟣 Roxo = Lojas
  - 🔴 Vermelho = Marcas
  - 🔵 Azul = Ordenação

### ⚡ Ações Rápidas
- **Selecionar Todos:** Marca todos os visíveis
- **Limpar:** Desmarca todos
- **Limpar Tudo:** Reseta toda a seleção

### 📊 Status em Tempo Real
- Loading overlay durante processamento
- Mensagens de sucesso/erro
- Contador de produtos encontrados
- Resumo de filtros aplicados

---

## 💡 Exemplos de Uso

### Exemplo 1: PS5 Original por Menor Preço
1. Buscar: "ps5"
2. Selecionar marca: "Sony"
3. Ordenação: "Menor Preço"
4. Aplicar filtros

### Exemplo 2: Produtos de Loja Específica
1. Buscar: "notebook"
2. Selecionar loja: "Atacado Connect"
3. Ordenação: "Mais Novos"
4. Aplicar filtros

### Exemplo 3: Múltiplas Lojas e Marcas
1. Buscar: "mouse"
2. Selecionar lojas: "Cellshop", "Star Games"
3. Selecionar marcas: "Logitech", "Razer"
4. Ordenação: "Menor Preço"
5. Aplicar filtros

---

## 🎯 Dicas Pro

### Para Melhores Ofertas:
- Sempre use ordenação "Menor Preço"
- Combine 2-3 lojas confiáveis
- Filtre por marca original

### Para Encontrar Lançamentos:
- Use ordenação "Mais Novos"
- Selecione marcas premium
- Verifique regularmente

### Para Comparar Preços:
- Não filtre por loja
- Use apenas marca + ordenação
- Compare resultados

### Para Busca Específica:
- Use campo de busca de filtros
- Digite parte do nome da loja/marca
- Economize tempo de scroll

---

## 📱 Interface Responsiva

A interface se adapta a:
- 💻 **Desktop:** Grade com múltiplas colunas
- 📱 **Tablet:** Grade responsiva
- 📱 **Mobile:** Coluna única otimizada

---

## ⚡ Atalhos de Teclado

- **Enter** no campo de busca → Executar busca
- **Tab** → Navegar entre campos
- **Espaço** → Selecionar checkbox focado

---

## 🎨 Código de Cores

### Mensagens:
- 🟢 Verde = Sucesso
- 🔴 Vermelho = Erro
- 🟡 Amarelo = Aviso

### Botões:
- 🟢 Verde = Ação principal
- 🔵 Azul = Ação secundária
- ⚫ Cinza = Limpar/Cancelar

---

## 🔧 Troubleshooting

### "Realize uma busca primeiro"
→ Digite um termo e clique em "Buscar"

### "Selecione pelo menos um filtro"
→ Marque checkboxes ou selecione ordenação

### "Sessão inválida ou expirada"
→ Faça uma nova busca

### Filtros não aparecem
→ Aguarde o loading completar (15-30s)

### Produtos não aparecem
→ Aguarde aplicação de filtros (10-20s)

---

## 📊 Métricas

Tempo médio por operação:
- Busca inicial: 15-30 segundos
- Aplicar filtros: 10-20 segundos
- Carregar produtos: 2-5 segundos

---

## 🚀 Comandos Úteis

### Iniciar servidor:
```powershell
python app.py
```

### Acessar interface:
```
http://localhost:5000
```

### Parar servidor:
```
Ctrl+C no terminal
```

---

## 📞 Suporte

Problemas? Verifique:
1. Servidor Flask está rodando?
2. Navegador suporta JavaScript?
3. Internet está funcionando?
4. Consulte logs no terminal

---

**Interface desenvolvida com Flask + Playwright + JavaScript**
**Totalmente funcional e pronta para uso!** ✨
