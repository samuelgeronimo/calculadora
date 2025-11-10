# 🚀 Guia de Deploy - Railway.app

## Por que Railway e não Vercel?

❌ **Vercel não funciona** porque:
- Não suporta Playwright (web scraping)
- Timeout de 10-60 segundos em serverless
- Não permite processos de background

✅ **Railway.app é perfeito** porque:
- Suporta Playwright com Chrome
- Sem limite de timeout
- Servidor persistente (não serverless)
- $5 de crédito grátis/mês

## 🔧 Passo a Passo

### 1. Criar conta no Railway
Acesse: https://railway.app/
- Login com GitHub (recomendado)
- Confirme email

### 2. Preparar repositório Git

```powershell
# Se ainda não tem Git iniciado
git init
git add .
git commit -m "Deploy inicial"

# Criar repositório no GitHub e conectar
git remote add origin https://github.com/SEU_USUARIO/calculadora.git
git push -u origin main
```

### 3. Deploy no Railway

1. No Railway Dashboard, clique **"New Project"**
2. Escolha **"Deploy from GitHub repo"**
3. Conecte sua conta GitHub (se necessário)
4. Selecione o repositório `calculadora`
5. Railway detectará automaticamente Python

### 4. Configurar Variáveis de Ambiente (Opcional)

No Railway Dashboard > Variables:
```
PORT=5000
PYTHONUNBUFFERED=1
```

### 5. Aguardar Build

O Railway vai:
- ✅ Instalar Python 3.12
- ✅ Instalar requirements.txt
- ✅ Instalar Playwright + Chromium
- ✅ Iniciar app.py
- ⏱️ Tempo: ~3-5 minutos

### 6. Acessar aplicação

Após deploy:
- Clique em **"Settings"** > **"Generate Domain"**
- Você receberá uma URL: `https://seu-projeto.up.railway.app`

## 📊 Monitoramento

### Logs em tempo real
Railway Dashboard > Deployments > View Logs

### Métricas
- CPU usage
- Memory usage
- Network traffic

## 💰 Custos

**Plano Hobby (Grátis):**
- $5 crédito/mês
- ~500 horas de execução
- Suficiente para uso pessoal/testes

**Se exceder:**
- Upgrade para Developer: $5/mês
- Ou otimize uso (desligue quando não usar)

## 🔄 Atualizações

Toda vez que fizer `git push`:
```powershell
git add .
git commit -m "Descrição da mudança"
git push
```

Railway redeploya automaticamente! 🚀

## 🐛 Troubleshooting

### Build falha
Verifique logs e certifique-se que:
- `requirements.txt` está correto
- `Procfile` existe
- `railway.json` está válido

### Timeout ao extrair produtos
- Normal na primeira execução (download do Chrome)
- Executações seguintes serão rápidas

### Memória insuficiente
Adicione no `railway.json`:
```json
"deploy": {
  "healthcheckPath": "/",
  "healthcheckTimeout": 300
}
```

## 📱 Alternativas

### Render.com (Similar ao Railway)
- $0 free tier (com limitações)
- Deploy: https://render.com

### Heroku (Pago)
- $5-7/mês mínimo
- Mais estável para produção

### VPS (Máximo controle)
- DigitalOcean: $4/mês
- Vultr: $2.50/mês
- Requer configuração manual

## ✅ Checklist Pre-Deploy

- [x] `requirements.txt` atualizado
- [x] `Procfile` criado
- [x] `railway.json` criado
- [x] `.railwayignore` criado
- [x] PORT dinâmico no app.py
- [x] Git inicializado
- [x] Código commitado
- [ ] Repositório GitHub criado
- [ ] Push para GitHub
- [ ] Deploy no Railway

## 🎯 Pronto para Deploy!

Siga os passos acima e sua aplicação estará online em minutos!