# Convert-to-Holytics

🎵 **Exportador de Músicas do Louvor JA para Holyrics**

Aplicação web moderna para exportar letras de músicas do banco de dados do Louvor JA (software Adventista) para arquivos `.txt` formatados, prontos para uso no Holyrics.

## ✨ Funcionalidades

- ✅ **Interface Web Moderna** - Design inspirado no Supabase Dashboard
- ✅ **Upload de Banco de Dados** - Importação fácil do database.db
- ✅ **Exportação em Lote** - Processa todas as músicas de uma vez
- ✅ **Progresso em Tempo Real** - Acompanhe a exportação ao vivo
- ✅ **Tabela Interativa** - Pesquise e visualize músicas exportadas
- ✅ **Preview de Letras** - Modal para visualizar antes de baixar
- ✅ **Download Individual** - Baixe músicas uma a uma
- ✅ **Download ZIP** - Baixe todas de uma vez
- ✅ **Dark Theme** - Interface moderna e confortável

## 🚀 Como Usar

### **Opção 1: Executar Localmente**

```bash
# 1. Clone o repositório
git clone https://github.com/RaphaelSchultz/Convert-to-Holytics.git
cd Convert-to-Holytics

# 2. Instale dependências
pip install -r requirements.txt

# 3. Execute
python run.py

# 4. Abra no navegador
http://localhost:5000
```

### **Opção 2: Docker**

```bash
# Build
docker-compose up --build

# Acesse
http://localhost:5000
```

## 📋 Requisitos

- Python 3.9+
- Flask 3.0+
- Banco de dados do Louvor JA (`database.db`)

## 🎯 Workflow

1. **Upload** do arquivo `database.db` do Louvor JA
2. **Clique** em "Iniciar Exportação"
3. **Aguarde** o processamento (barra de progresso)
4. **Visualize** a tabela com as músicas exportadas
5. **Download** individual ou ZIP completo

## 📁 Estrutura

```
Convert-to-Holytics/
├── app/                    # Aplicação Flask
│   ├── routes/            # Rotas e endpoints
│   ├── services/          # Lógica de negócio
│   ├── repositories/      # Acesso a dados
│   └── utils/             # Utilitários
├── static/                # CSS e JavaScript
├── templates/             # HTML
├── musicas_txt_formatadas/ # Arquivos exportados
└── run.py                 # Entry point
```

## 🎨 Design

Interface moderna com:
- **Supabase-inspired** dark theme
- **Verde vibrante** (#3ECF8E) como cor principal
- **Tipografia** Inter (Google Fonts)
- **Componentes** responsivos e acessíveis

## 📝 Formato dos Arquivos

Os arquivos `.txt` exportados contêm:
```
Título: [Nome da Música]
Artista: [Álbum/Artista]

[Letra formatada em estrofes]
```

**Hinário Adventista**: Inclui número da música no nome do arquivo
- Exemplo: `001 - Santo, Santo, Santo! (Hinario Adventista).txt`

**Outras músicas**: Nome + ID único
- Exemplo: `Grande e o Senhor - 123.txt`

## 🔧 Configuração

Variáveis de ambiente (opcional):
```env
SECRET_KEY=your-secret-key
FLASK_ENV=development
HOST=0.0.0.0
PORT=5000
```

## 📦 Deploy

### **Heroku**
```bash
git push heroku main
```

### **Docker**
```bash
docker build -t convert-to-holytics .
docker run -p 5000:5000 convert-to-holytics
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📄 Licença

Este projeto é código aberto e está disponível sob a [MIT License](LICENSE).

## 👨‍💻 Autor

Desenvolvido com ❤️ para a comunidade Adventista

---

**Nota**: Este projeto foi criado para facilitar a exportação de músicas do Louvor JA para o Holyrics. Não é afiliado oficialmente com nenhum dos softwares mencionados.
