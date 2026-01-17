# 🌍 Deploy GRÁTIS para Leigos - PythonAnywhere

## 🎯 Resultado Final

Após seguir este guia, você terá:
```
https://seu-usuario.pythonanywhere.com
```

**Qualquer pessoa** pode acessar essa URL e usar o app! Sem instalar nada! 🎉

---

## 📋 Passo a Passo (15 minutos)

### **1️⃣ Criar Conta Gratuita**

1. Acesse: **https://www.pythonanywhere.com**
2. Clique em **"Pricing & signup"**
3. Escolha **"Create a Beginner account"** (100% grátis)
4. Preencha:
   - Username (será sua URL: `username.pythonanywhere.com`)
   - Email
   - Senha
5. Confirme email

---

### **2️⃣ Fazer Upload dos Arquivos**

1. **Login** em pythonanywhere.com
2. Vá em **"Files"** (menu superior)
3. Clique em **"Upload a file"**
4. Faça upload de **TODOS** esses arquivos/pastas:

```
✅ app/ (pasta inteira)
✅ static/ (pasta inteira)
✅ templates/ (pasta inteira)
✅ run.py
✅ requirements.txt
✅ .env (opcional)
```

**Dica**: Comprima tudo em um `.zip` e extraia lá dentro.

---

### **3️⃣ Instalar Dependências**

1. Vá em **"Consoles"** (menu superior)
2. Clique em **"Bash"**
3. Digite:

```bash
pip install --user -r requirements.txt
```

Aguarde terminar (1-2 min)

---

### **4️⃣ Configurar Web App**

1. Vá em **"Web"** (menu superior)
2. Clique em **"Add a new web app"**
3. Escolha:
   - Next → Next
   - **"Manual configuration"**
   - **Python 3.10**
4. Clique em **"Next"**

---

### **5️⃣ Configurar WSGI**

1. Na página Web, encontre **"Code"** → **"WSGI configuration file"**
2. Clique no link (algo como `/var/www/username_pythonanywhere_com_wsgi.py`)
3. **Delete TUDO** e cole:

```python
import sys
import os

# Adicione o diretório do projeto
project_home = '/home/SEU_USERNAME'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Importe a aplicação
from run import app as application
```

**⚠️ IMPORTANTE**: Substitua `SEU_USERNAME` pelo seu username!

4. Clique em **"Save"**

---

### **6️⃣ Definir Diretórios**

1. Volte para a aba **"Web"**
2. Em **"Code"**, configure:

**Source code:**
```
/home/SEU_USERNAME
```

**Working directory:**
```
/home/SEU_USERNAME
```

3. Em **"Static files"**, adicione:

**URL:** `/static/`  
**Directory:** `/home/SEU_USERNAME/static`

4. Clique em **"Save"** (canto superior direito)

---

### **7️⃣ Recarregar Web App**

1. No topo da página **"Web"**
2. Clique no botão verde **"Reload seu-usuario.pythonanywhere.com"**

---

### **8️⃣ Acessar a Aplicação**

Sua URL:
```
https://seu-usuario.pythonanywhere.com
```

**Pronto!** 🎊 Compartilhe essa URL com qualquer pessoa!

---

## 🔧 Solução de Problemas

### **Erro: Application failed to start**
1. Vá em **"Web"** → **"Error log"**
2. Veja o erro
3. Geralmente é:
   - Username errado no WSGI
   - Dependências não instaladas

### **Erro: 502 Bad Gateway**
- Aguarde 1-2 minutos após Reload
- Se persistir, veja Error log

### **Atualizar Código**
1. Faça upload dos arquivos novos
2. Vá em **"Web"** → **"Reload"**

---

## 📝 Limitações (Free Tier)

- ✅ **Banda ilimitada**
- ✅ **HTTPS grátis**
- ✅ **Storage**: 512 MB
- ⚠️ **CPU**: 100 segundos/dia
- ⚠️ App **dorme** após inatividade (acorda ao acessar)

**Para este projeto:** CPU suficiente para ~50-100 exportações/dia.

---

## 🎥 Tutorial em Vídeo (Opcional)

Se quiser, grave você mesmo fazendo isso e compartilhe:
- **Loom**: https://loom.com (grátis, fácil)
- **YouTube**: Upload privado/não listado

---

## ✅ Checklist Rápido

- [ ] Conta criada no PythonAnywhere
- [ ] Arquivos uploaded
- [ ] `pip install -r requirements.txt` executado
- [ ] Web app criado
- [ ] WSGI configurado (com username correto)
- [ ] Diretórios configurados
- [ ] App recarregado
- [ ] URL funcionando
- [ ] **Compartilhado!** 🚀

---

**Precisa de ajuda?** Me chame! Vou te guiar passo a passo! 💪
