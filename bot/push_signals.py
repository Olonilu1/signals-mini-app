"""Push unpushed signals from data/signals.json to every subscriber."""
import asyncio
import json
import os
from html import escape
from pathlib import Path

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter

DATA = Path(__file__).resolve().parent.parent / "data"


def render(signal: dict) -> str:
    why = escape(str(signal.get("why", "")))
    return (
        f"<b>{escape(signal['symbol'])} {escape(signal['direction'])}</b> - Crosser\n"
        f"Entry {escape(str(signal['entry']))} | TP {escape(str(signal['tp']))} | SL {escape(str(signal['sl']))}\n"
        f"<i>{why}</i>"
    )


async def main() -> None:
    token = os.environ.get("BOT_TOKEN", "")
    if not token:
        raise SystemExit("BOT_TOKEN is not set")
    signals = json.loads((DATA / "signals.json").read_text())
    subs = json.loads((DATA / "subscribers.json").read_text())
    pending = [s for s in signals if not s.get("pushed")]
    if not pending or not subs:
        print("nothing to push")
        return
    bot = Bot(token)
    sent = 0
    for signal in pending:
        text = render(signal)
        for user_id in subs:
            try:
                await bot.send_message(user_id, text)
            except TelegramRetryAfter as err:
                await asyncio.sleep(err.retry_after)
                await bot.send_message(user_id, text)
        signal["pushed"] = True
        sent += 1
    (DATA / "signals.json").write_text(json.dumps(signals, indent=2))
    print(f"pushed {sent} signal(s) to {len(subs)} subscriber(s)")


if __name__ == "__main__":
    asyncio.run(main())
