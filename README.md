# SKALLA API (FastAPI + Postgres + Docker + Nginx + Alembic)

Sistema de gerenciamento de voluntários para igrejas com integração WhatsApp.

## 🚀 Rodar localmente com Docker

1. Copie o arquivo de exemplo e configure suas variáveis:
   ```bash
   cp .env.example .env
   ```

2. Edite o `.env` e adicione seus tokens:
   - `VERIFY_TOKEN`: Token para verificação do webhook
   - `WHATSAPP_TOKEN`: Token da API do WhatsApp Business
   - `WHATSAPP_PHONE_NUMBER_ID`: ID do número do WhatsApp
   - `WEBHOOK_SECRET`: Segredo para webhook
   - `OPENAI_API_KEY` (opcional): Chave da API OpenAI

3. Inicie os containers:
   ```bash
   docker compose up -d --build
   ```

4. Acesse a documentação interativa:
   - Local: http://localhost:8000/docs
   - Produção: https://api.skalla.pt/docs

## 📋 Endpoints principais

### Gerenciamento
- `POST /churches` - Criar igreja
- `GET /churches/{id}` - Obter igreja
- `POST /volunteers` - Criar voluntário
- `POST /departments` - Criar departamento
- `POST /schedules` - Criar escala
- `POST /schedule-assignments` - Atribuir voluntário à escala

### Webhook WhatsApp
- `GET /webhook` - Verificação Meta (Facebook)
- `POST /webhook` - Receber mensagens do WhatsApp

### Logs
- `GET /logs` - Listar últimos 200 logs

## 🗄️ Banco de dados

As migrações são executadas automaticamente ao iniciar o container via `entrypoint.sh`.

Para criar uma nova migração:
```bash
docker compose exec api alembic revision -m "descricao"
```

## 🔒 Segurança

**IMPORTANTE:**
- ✅ Mantenha tokens APENAS no arquivo `.env`
- ✅ Nunca commite o arquivo `.env` no Git
- ✅ Use `.env.example` como template
- ✅ Rotacione tokens periodicamente

## 📦 Estrutura do projeto

```
skalla-api/
├── app/
│   ├── models/          # Modelos SQLAlchemy
│   ├── routers/         # Endpoints FastAPI
│   ├── services/        # Lógica de negócio
│   ├── database.py      # Configuração DB
│   ├── settings.py      # Variáveis de ambiente
│   └── main.py          # App principal
├── alembic/             # Migrações
├── scripts/             # Scripts de inicialização
├── nginx/               # Configuração Nginx
└── docker-compose.yml   # Orquestração containers
```

## 🛠️ Desenvolvimento

Para desenvolvimento local sem Docker:

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar migrações
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

## 📝 Licença

Projeto privado - Todos os direitos reservados.
