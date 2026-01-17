# Deploy para Vercel

## 📋 Pré-requisitos

- Conta no [Vercel](https://vercel.com)
- Repositório GitHub já configurado ✅

## 🚀 Passos para Deploy

### 1. Acessar Vercel

1. Acesse [vercel.com](https://vercel.com)
2. Faça login com sua conta GitHub

### 2. Importar Projeto

1. Clique em **"Add New..."** → **"Project"**
2. Selecione o repositório: `RaphaelSchultz/Convert-to-Holytics`
3. Clique em **"Import"**

### 3. Configurar Projeto

**Framework Preset**: Other

**Build Settings**:
- Build Command: (deixe vazio)
- Output Directory: (deixe vazio)
- Install Command: `pip install -r requirements.txt`

**Environment Variables** (opcional):
- `SECRET_KEY`: `sua-chave-secreta-aqui`
- `FLASK_ENV`: `production`

### 4. Deploy

1. Clique em **"Deploy"**
2. Aguarde o build (1-2 minutos)
3. Projeto estará disponível em: `https://convert-to-holytics.vercel.app`

### 5. Configurar Domínio Personalizado

1. No dashboard do projeto, vá em **"Settings"** → **"Domains"**
2. Digite: `musicasja`
3. Vercel irá sugerir: `musicasja.vercel.app`
4. Clique em **"Add"**
5. Aguarde a propagação (alguns segundos)

✅ Seu app estará disponível em: **https://musicasja.vercel.app**

## ⚠️ Limitações do Vercel (Free Tier)

- **Tempo de execução**: 10 segundos max por request
- **Tamanho do payload**: 4.5 MB
- **Memória**: 1024 MB

### ⚠️ Importante para este Projeto:

Este projeto **pode ter problemas no Vercel** porque:
1. Exportação de 1550 músicas pode levar **mais de 10 segundos**
2. Arquivos grandes podem exceder limite de payload

### 💡 Alternativas Recomendadas:

Se o Vercel não funcionar bem:

1. **Railway** (recomendado):
   - Sem limite de tempo de execução
   - Melhor para processamento longo
   - Deploy: `railway up`

2. **Render**:
   - Free tier com 15 minutos de timeout
   - Boa para Flask apps

3. **Heroku**:
   - Você já tem o `Procfile` configurado
   - Deploy via Git

## 🧪 Testando Deploy

Após deploy, teste:
1. Acesse a URL
2. Faça upload de um arquivo pequeno
3. Exporte algumas músicas
4. Verifique se o download funciona

## 📝 Notas

- Arquivos exportados são temporários no Vercel (serverless)
- Para produção séria, considere Railway ou Render
- Mantenha o GitHub atualizado: `git push origin main`
