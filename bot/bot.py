"""Signals bot: /start registers the subscriber and shows the Mini App button."""
import asyncio
import json
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

DATA = Path(__file__).resolve().parent.parent / "data"
SUBS_FILE = DATA / "subscribers.json"
WEBAPP_URL = os.environ.get("WEBAPP_URL", "")


def load_subs() -> list[int]:
    try:
        return json.loads(SUBS_FILE.read_text())
    except (OSError, ValueError):
        return []


def save_subs(subs: list[int]) -> None:
    DATA.mkdir(exist_ok=True)
    SUBS_FILE.write_text(json.dumps(sorted(set(subs))))


async def main() -> None:
    token = os.environ.get("BOT_TOKEN", "")
    if not token:
        raise SystemExit("BOT_TOKEN is not set")
    if not WEBAPP_URL:
        raise SystemExit("WEBAPP_URL is not set (https URL of the dashboard)")

    bot = Bot(token)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message) -> None:
        subs = load_subs()
        if message.from_user and message.from_user.id not in subs:
            subs.append(message.from_user.id)
            save_subs(subs)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Open signals", web_app=WebAppInfo(url=WEBAPP_URL))]
            ]
        )
        await message.answer(
            "Live Crosser signal dashboard. Tap below to open it.",
            reply_markup=keyboard,
        )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
