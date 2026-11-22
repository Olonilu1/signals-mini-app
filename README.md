# signals-mini-app

Telegram Mini App dashboard for live Crosser trading signals, plus a bot that
subscribes people and pushes new signals to them. Built with guidance from
[bisnuray/telegram-craft](https://github.com/bisnuray/telegram-craft).

## What is inside

- `webapp/index.html` - the Mini App dashboard (dark, mobile-first, polls every 30 s)
- `server/app.py` - FastAPI server: serves the dashboard and the `/api/signals` JSON API
- `bot/bot.py` - aiogram bot: `/start` subscribes the user and shows the Mini App button
- `bot/push_signals.py` - pushes unpushed signals from `data/signals.json` to subscribers
- `data/signals.json` - signal list (sample data included)

Signal shape: `{symbol, direction, entry, tp, sl, candle_open, why, pushed}`.

## Run locally

```bash
pip install -r requirements.txt
uvicorn server.app:app --reload           # dashboard on http://127.0.0.1:8000
BOT_TOKEN=... WEBAPP_URL=https://your-host python3 bot/bot.py
python3 bot/push_signals.py
```

## Going live

1. Create a bot with @BotFather, save the token.
2. Host `server/app.py` on any HTTPS host (Render/Fly/Vercel with an ASGI adapter);
   set that HTTPS URL as `WEBAPP_URL` and as the bot's Menu Button / Web App URL.
3. Set `API_TOKEN` on the server and post new signals from your scan:
   `curl -X POST $WEBAPP_URL/api/signals -H "X-API-Token: $API_TOKEN" -H "Content-Type: application/json" -d '{...}'`
   then run `bot/push_signals.py` to broadcast them.
4. In BotFather, `/setmenubutton` with the Mini App URL so users get the dashboard button.

## Status

- Local server tested: `GET /api/signals` returns the sample data.
- Bot code is written for a real token but has NOT run against Telegram yet (needs your BotFather token).
