# Bot Telegram de Análise Gramatical de Áudio

Este projeto é um bot do Telegram que recebe áudios, transcreve o conteúdo, identifica o idioma (português ou inglês), analisa gramaticalmente usando IA (Groq) e retorna ao usuário a porcentagem de acerto e os erros gramaticais encontrados.

## Funcionalidades
- Recebe áudios via Telegram
- Transcreve o áudio para texto
- Detecta automaticamente o idioma (português ou inglês)
- Analisa gramaticalmente o texto usando IA
- Retorna porcentagem de acerto e lista de erros gramaticais

## Como rodar localmente

### 1. Clone o repositório
```bash
git clone <url-do-repo>
cd projeto_ia_telegram
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Crie um arquivo `.env` baseado no exemplo `.env.example`:

```
TELEGRAM_BOT_TOKEN=seu_token_do_telegram
GROQ_API_KEY=sua_api_key_groq
```

### 4. Rode o bot
```bash
python bot.py
```

## Como obter as chaves
- **TELEGRAM_BOT_TOKEN**: Crie um bot no Telegram falando com o [@BotFather](https://t.me/BotFather) e obtenha o token.
- **GROQ_API_KEY**: Crie uma conta em https://groq.com/ e gere uma API Key.

## Hospedagem gratuita
Você pode hospedar este bot gratuitamente em plataformas como:
- [Railway](https://railway.app/)
- [Render](https://render.com/)

Basta criar um novo projeto, subir o código, definir as variáveis de ambiente e rodar o comando:
```
python bot.py
```

## Observações
- O bot aceita apenas mensagens de voz (áudio).
- O tempo de resposta depende do tamanho do áudio e da resposta da IA.
- O bot identifica automaticamente se o áudio está em português ou inglês.

---

Feito com ❤️ para análise gramatical inteligente! 