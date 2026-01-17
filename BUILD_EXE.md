# 🚀 Criar Executável Windows (.exe)

## 📦 Instalação do PyInstaller

```powershell
pip install pyinstaller
```

## 🔨 Gerar o Executável

### Opção 1: Usando o Script Pronto

```powershell
.\build_exe.bat
```

### Opção 2: Comando Manual

```powershell
pyinstaller Convert-to-Holytics.spec
```

## 📂 Onde Encontrar o .exe

Após build (1-2 minutos):
```
dist/Convert-to-Holytics.exe
```

## ✅ Como Usar

1. **Copie** `Convert-to-Holytics.exe` para onde quiser
2. **Duplo clique** no .exe
3. **Aguarde** ~5 segundos
4. **Navegador abre automaticamente** em `http://127.0.0.1:5000`

**PRONTO!** Não precisa instalar Python ou dependências! 🎉

## 📝 Notas

- **Tamanho**: ~80-100 MB (inclui Python + Flask + tudo)
- **Console**: Mostra logs (pode minimizar)
- **Porta**: 5000 (se estiver ocupada, mude no `launcher.py`)
- **Antivírus**: Pode dar alerta falso (é normal com PyInstaller)

## 🎁 Distribuir

Para distribuir para outras pessoas:
1. Envie apenas o `Convert-to-Holytics.exe`
2. Eles dão duplo clique
3. Funciona sem instalar nada!

## 🐛 Problemas Comuns

### "Arquivo muito grande"
- Normal! Inclui Python inteiro
- Use UPX para comprimir (já configurado)

### "Antivírus bloqueou"
- Adicione exceção
- Ou assine digitalmente o .exe

### "Porta 5000 em uso"
- Mude porta no `launcher.py` linha 30
- Recompile

## 🔄 Rebuild Após Mudanças

Se mudar código:
```powershell
.\build_exe.bat
```

Novo .exe gerado em `dist/`
