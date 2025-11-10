# Vercel não suporta este projeto

Este projeto usa **Playwright** para web scraping, que requer:
- Navegador Chrome/Chromium
- Processos de longa duração
- Operações assíncronas complexas

**Vercel é serverless** e tem limitações:
- ❌ Timeout máximo: 10s (hobby) ou 60s (pro)
- ❌ Não permite instalação de navegadores
- ❌ Ambiente efêmero (não mantém estado)

## ✅ Use Railway.app em vez disso

Veja o arquivo **DEPLOY.md** para instruções completas.

### Deploy rápido:
1. Crie conta em https://railway.app
2. Conecte repositório GitHub
3. Railway faz deploy automático
4. Pronto! ✨

Railway suporta Playwright e é gratuito para começar ($5 crédito/mês).