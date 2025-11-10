# 🚀 Próximos Passos - Deploy

## ✅ Git Configurado!

Repositório local criado e conectado a:
`https://github.com/samuelgeronimo/calculadora`

## 📤 Para enviar ao GitHub:

### 1. Criar o repositório no GitHub (se ainda não criou)

Acesse: https://github.com/new

- **Nome**: `calculadora`
- **Descrição**: Sistema de extração de produtos com calculadora de preços
- **Visibilidade**: Private ou Public (sua escolha)
- ⚠️ **NÃO** marque "Initialize with README" (já temos)

### 2. Enviar código

```powershell
git push -u origin main
```

Se pedir autenticação, use **Personal Access Token**:
- Acesse: https://github.com/settings/tokens
- Generate new token (classic)
- Marque: `repo` (full control)
- Use o token como senha

## 🚂 Deploy no Railway

### 1. Acesse Railway
https://railway.app

### 2. Login com GitHub
- Autorize Railway acessar seus repositórios

### 3. Novo Projeto
- Click **"New Project"**
- Escolha **"Deploy from GitHub repo"**
- Selecione `samuelgeronimo/calculadora`

### 4. Aguarde Build
Railway vai automaticamente:
- ✅ Detectar Python
- ✅ Ler `railway.json`
- ✅ Instalar requirements
- ✅ Instalar Playwright + Chromium
- ✅ Iniciar aplicação

⏱️ Tempo: ~3-5 minutos

### 5. Gerar Domínio
- Settings > Networking
- Click **"Generate Domain"**
- Sua URL: `https://calculadora-production-XXXX.up.railway.app`

## 🎯 Pronto!

Seu sistema estará online e acessível publicamente! 🌐

## 📊 Monitoramento

No Railway Dashboard você pode ver:
- Logs em tempo real
- Uso de CPU/Memória
- Requisições
- Erros

## 💰 Custos

**Plano Hobby**: $5 grátis/mês (~500 horas)
Suficiente para uso pessoal/testes!

---

**Dúvidas?** Veja o arquivo `DEPLOY.md` completo.