# 🎵 Convert to Holytics

> **API Flask para exportar músicas do banco de dados Louvor JA para arquivos .txt formatados**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Descrição

O **Convert to Holytics** é uma API REST construída com Flask que permite exportar letras de músicas do software **Louvor JA** (Jovens Adventistas) para arquivos de texto formatados. O sistema oferece controle completo sobre o processo de exportação, incluindo progresso em tempo real e capacidade de cancelamento.

### ✨ Features

- ✅ **Exportação Completa**: Extrai todas as músicas do banco de dados Louvor JA
- ✅ **Formatação Inteligente**: Remove acentos e formata letras em blocos legíveis
- ✅ **Progresso em Tempo Real**: Acompanhe o andamento via endpoint `/status`
- ✅ **Cancelamento Controlado**: Pare a exportação a qualquer momento
- ✅ **Thread-Safe**: Sistema robusto com locks para operações concorrentes
- ✅ **Logging Completo**: Rastreamento detalhado de todas as operações
- ✅ **Validação de Segurança**: Proteção contra path traversal attacks
- ✅ **CORS Habilitado**: Pronto para integração com frontends
- ✅ **Multi-Plataforma**: Funciona em Windows, Linux e macOS

---

## 🚀 Instalação Local

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Banco de dados do Louvor JA (`database.db`)

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/RaphaelSchultz/Convert-to-Holytics.git
   cd Convert-to-Holytics
   ```

2. **Crie um ambiente virtual** (recomendado)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   # Copie o arquivo de exemplo
   cp .env.example .env
   
   # Edite o .env e ajuste o caminho do banco de dados
   # Windows: DEFAULT_DB_PATH=C:\Program Files (x86)\Louvor JA\config\database.db
   # Linux/Mac: Ajuste conforme sua instalação
   ```

5. **Execute o servidor**
   ```bash
   python app.py
   ```

   O servidor estará disponível em `http://localhost:5000`

---

## 📡 API Endpoints

### `GET /`
Retorna informações sobre a API e endpoints disponíveis.

**Resposta:**
```json
{
  "name": "Convert to Holytics API",
  "version": "1.0.0",
  "description": "API para exportar músicas do Louvor JA",
  "endpoints": { ... }
}
```

---

### `POST /start`
Inicia o processo de exportação.

**Body (JSON):**
```json
{
  "db_path": "C:\\Program Files (x86)\\Louvor JA\\config\\database.db"
}
```

**Resposta de Sucesso (200):**
```json
{
  "message": "Exportação iniciada",
  "status": {
    "running": true,
    "progress": 0,
    "total": 0,
    "message": "Iniciando exportação..."
  }
}
```

**Erros:**
- `400`: Exportação já em andamento ou caminho inválido
- `400`: Arquivo não encontrado ou extensão inválida

---

### `GET /status`
Retorna o status atual da exportação.

**Resposta:**
```json
{
  "running": true,
  "progress": 45,
  "total": 150,
  "message": "Exportando música 45 de 150..."
}
```

---

### `POST /cancel`
Cancela a exportação em andamento.

**Resposta de Sucesso (200):**
```json
{
  "message": "Solicitação de cancelamento enviada",
  "status": {
    "running": false,
    "message": "Cancelando exportação..."
  }
}
```

**Erros:**
- `400`: Nenhuma exportação em andamento

---

### `GET /health`
Health check endpoint para monitoramento.

**Resposta:**
```json
{
  "status": "healthy",
  "service": "convert-to-holytics",
  "version": "1.0.0"
}
```

---

## 🐳 Docker (Deployment)

### Build da Imagem
```bash
docker build -t convert-to-holytics .
```

### Executar Container
```bash
docker run -p 5000:5000 \
  -v /path/to/database.db:/app/database.db \
  -e DEFAULT_DB_PATH=/app/database.db \
  convert-to-holytics
```

### Docker Compose
```bash
docker-compose up -d
```

---

## ☁️ Deploy em Produção

### Heroku

1. **Login e criação do app**
   ```bash
   heroku login
   heroku create seu-app-name
   ```

2. **Deploy**
   ```bash
   git push heroku main
   ```

3. **Configurar variáveis de ambiente**
   ```bash
   heroku config:set DEFAULT_DB_PATH=/path/to/database.db
   heroku config:set LOG_LEVEL=INFO
   ```

### Railway

1. Conecte seu repositório GitHub ao Railway
2. Configure as variáveis de ambiente no dashboard:
   - `DEFAULT_DB_PATH`
   - `PORT` (Railway fornece automaticamente)
3. Deploy automático a cada push

### Vercel (Limitado para Flask)

> ⚠️ Nota: Vercel é otimizado para serverless. Para Flask, considere Railway ou Heroku.

---

## ⚙️ Configuração (.env)

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `FLASK_ENV` | Ambiente (development/production) | `development` |
| `FLASK_DEBUG` | Modo debug | `True` |
| `HOST` | Host do servidor | `0.0.0.0` |
| `PORT` | Porta do servidor | `5000` |
| `DEFAULT_DB_PATH` | Caminho padrão do banco | Windows: `C:\Program Files (x86)\Louvor JA\config\database.db` |
| `OUTPUT_DIR` | Diretório de saída | `musicas_txt_formatadas` |
| `CORS_ORIGINS` | Origens permitidas para CORS | `*` |
| `LOG_LEVEL` | Nível de log (DEBUG/INFO/WARNING/ERROR) | `INFO` |
| `LOG_FILE` | Arquivo de log | `app.log` |

---

## 📂 Estrutura do Projeto

```
Convert-to-Holytics/
├── app.py                      # API Flask principal
├── exportar_musicas.py         # Lógica de exportação
├── requirements.txt            # Dependências Python
├── .env.example                # Exemplo de configuração
├── .gitignore                  # Arquivos ignorados pelo Git
├── Procfile                    # Config para Heroku
├── README.md                   # Este arquivo
└── musicas_txt_formatadas/     # Diretório de saída (gerado)
```

---

## 🔒 Segurança

O projeto implementa as seguintes medidas de segurança:

- ✅ **Validação de Path**: Previne path traversal attacks
- ✅ **Type Hints**: Validação de tipos em tempo de desenvolvimento
- ✅ **Queries Parametrizadas**: Proteção contra SQL injection
- ✅ **Sanitização de Nomes**: Remove caracteres perigosos de nomes de arquivo
- ✅ **Thread Safety**: Locks para prevenir race conditions
- ✅ **CORS Configurável**: Controle de origens permitidas

---

## 🐛 Troubleshooting

### Erro: "No module named 'flask_cors'"
```bash
pip install flask-cors
```

### Erro: "Arquivo não encontrado: database.db"
Verifique o caminho no `.env` ou no body da requisição POST.

### Erro: "Exportação já em andamento"
Cancele a exportação atual com `POST /cancel` ou aguarde a conclusão.

### Porta 5000 já em uso
Altere a porta no `.env`:
```env
PORT=8000
```

---

## 📊 Formato dos Arquivos Exportados

Cada música é exportada como um arquivo `.txt` com o seguinte formato:

```
Título: Nome da Música
Artista: Nome do Álbum

Estrofe 1
Linha 1
Linha 2

Estrofe 2
Linha 1
Linha 2
```

- Nomes de arquivo são sanitizados (sem caracteres especiais)
- Acentos são removidos
- Músicas do Hinário Adventista são identificadas com sufixo

---

## 🛠️ Desenvolvimento

### Executar em Modo Debug
```bash
export FLASK_DEBUG=True  # Linux/Mac
set FLASK_DEBUG=True     # Windows
python app.py
```

### Logs
Os logs são salvos em `app.log` e também exibidos no console.

---

## 📝 Changelog

### v1.0.0 (Janeiro 2026)
- ✅ Implementação inicial da API
- ✅ Thread safety com locks
- ✅ Sistema de logging completo
- ✅ Validação de paths
- ✅ CORS habilitado
- ✅ Suporte multi-plataforma
- ✅ Documentação completa

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Raphael Schultz**
- GitHub: [@RaphaelSchultz](https://github.com/RaphaelSchultz)

---

## 🙏 Agradecimentos

- Comunidade Jovens Adventistas
- Software Louvor JA
- Comunidade Flask

---

## 📞 Suporte

Se você encontrar problemas ou tiver perguntas:

1. Verifique a seção [Troubleshooting](#-troubleshooting)
2. Consulte os [logs](#-desenvolvimento)
3. Abra uma [Issue](https://github.com/RaphaelSchultz/Convert-to-Holytics/issues)

---

**Feito com ❤️ para a comunidade Adventista**
