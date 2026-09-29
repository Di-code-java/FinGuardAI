import asyncio


from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import BOT_TOKEN
from api import get_price
from formatter import clean_ai_text

from config import BOT_TOKEN
from api import get_price
from aiogram import (
    Bot,
    Dispatcher,
    F
)

from aiogram.filters import Command

from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from config import BOT_TOKEN

from api import (
    get_market_analysis
)

from ai import (
    ask_ai,
    analyze_market
)


# ============================================================
# BOT
# ============================================================

bot = Bot(
    token=BOT_TOKEN
)

dp = Dispatcher()


# ============================================================
# КЛАВИАТУРА
# ============================================================

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="📊 Анализ актива"
            ),
            KeyboardButton(
                text="🤖 AI-вопрос"
            )
        ],

        [
            KeyboardButton(
                text="🔍 Проверить BTC"
            ),
            KeyboardButton(
                text="🔍 Проверить ETH"
            )
        ],

        [
            KeyboardButton(
                text="🧮 Калькулятор"
            ),
            KeyboardButton(
                text="🌐 Актуальный поиск"
            )
        ],

        [
            KeyboardButton(
                text="ℹ️ Помощь"
            )
        ]
    ],

    resize_keyboard=True
)


# ============================================================
# ДЛИННЫЕ СООБЩЕНИЯ
# ============================================================

def split_message(
    text,
    max_length=3800
):

    return [
        text[i:i + max_length]
        for i in range(
            0,
            len(text),
            max_length
        )
    ]


async def send_long_message(
    message,
    text
):

    parts = split_message(text)

    for part in parts:

        await message.answer(part)


# ============================================================
# START
# ============================================================

@dp.message(Command("start"))
async def start_command(message: Message):

    await message.answer(
        "🛡️ FinGuard AI\n\n"
        "Интеллектуальный финансовый помощник.\n\n"
        "Я умею:\n"
        "📊 анализировать криптовалюты\n"
        "🤖 отвечать на финансовые вопросы\n"
        "🧮 выполнять финансовые расчёты\n"
        "🌐 искать актуальную и историческую информацию\n"
        "⚠️ выявлять потенциальные рыночные аномалии\n\n"
        "Выберите действие ниже:",
        reply_markup=main_keyboard
    )


# ============================================================
# HELP
# ============================================================

@dp.message(
    Command("help")
)
async def help_command(message: Message):

    await message.answer(
        "ℹ️ FinGuard AI\n\n"

        "📊 Анализ актива\n"
        "Введите BTC, ETH или другой актив.\n\n"

        "🤖 AI-вопрос\n"
        "Задайте финансовый вопрос обычным языком.\n\n"

        "🧮 Калькулятор\n"
        "Например:\n"
        "«1 000 000 ₸ под 15% на 3 года»\n\n"

        "🌐 Актуальный поиск\n"
        "Например:\n"
        "«Какая сейчас ставка по депозитам?»\n\n"

        "Исторические данные также поддерживаются."
    )


# ============================================================
# BTC
# ============================================================

@dp.message(
    F.text == "🔍 Проверить BTC"
)
async def btc_button(message: Message):

    await scan_asset(
        message,
        "BTC"
    )


# ============================================================
# ETH
# ============================================================

@dp.message(
    F.text == "🔍 Проверить ETH"
)
async def eth_button(message: Message):

    await scan_asset(
        message,
        "ETH"
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

@dp.message(
    F.text == "📊 Анализ актива"
)
async def analyze_button(message: Message):

    await message.answer(
        "📊 Напишите тикер актива.\n\n"
        "Например:\n"
        "BTC\n"
        "ETH\n"
        "SOL"
    )


# ============================================================
# AI BUTTON
# ============================================================

@dp.message(
    F.text == "🤖 AI-вопрос"
)
async def ai_button(message: Message):

    await message.answer(
        "🤖 Задайте финансовый вопрос.\n\n"
        "Например:\n\n"
        "Почему растёт объём BTC?\n\n"
        "Что такое финансовый пузырь?\n\n"
        "Как работает сложный процент?"
    )


# ============================================================
# CALCULATOR BUTTON
# ============================================================

@dp.message(
    F.text == "🧮 Калькулятор"
)
async def calculator_button(message: Message):

    await message.answer(
        "🧮 Финансовый калькулятор\n\n"

        "Пишите расчёт обычным языком.\n\n"

        "Примеры:\n\n"

        "15% от 500000\n\n"

        "Депозит 1000000 под 15% "
        "и пополняю 50000 каждый месяц "
        "3 года\n\n"

        "Кредит 5000000 под 18% "
        "на 5 лет\n\n"

        "Упал на 40%, сколько нужно "
        "для восстановления?"
    )


@dp.message(Command("ask"))
async def ask_command(message: Message):
    question = message.text.replace("/ask", "").strip()

    if not question:
        await message.answer("❗ Напиши вопрос после /ask")
        return

    result = await get_ai_answer(question)

    result = clean_ai_text(result)

    await message.answer(result)

# ============================================================
# SEARCH BUTTON
# ============================================================

@dp.message(
    F.text == "🌐 Актуальный поиск"
)
async def search_button(message: Message):

    await message.answer(
        "🌐 Напишите финансовый вопрос.\n\n"

        "Например:\n\n"

        "Какая сейчас ставка по депозитам Halyk Bank?\n\n"

        "Какой курс USD/KZT сегодня?\n\n"

        "Какие ставки были в 2024 году?"
    )


# ============================================================
# HELP BUTTON
# ============================================================

@dp.message(
    F.text == "ℹ️ Помощь"
)
async def help_button(message: Message):

    await help_command(message)


# ============================================================
# SCAN ASSET
# ============================================================

async def scan_asset(
    message: Message,
    symbol: str
):

    await message.answer(
        f"🔎 Анализирую {symbol}..."
    )

    try:

        data = await get_market_analysis(
            symbol
        )

        text = (
            "📊 FinGuard AI\n\n"

            f"🪙 {data['symbol']}\n\n"

            f"💰 Цена: "
            f"{data['price']:.8f}\n"

            f"📈 24ч: "
            f"{data['change_24h']:.2f}%\n"

            f"📦 Объём: "
            f"{data['volume']:.2f}\n\n"

            f"📊 SMA20: "
            f"{data['sma20']:.4f}\n"

            f"📊 SMA50: "
            f"{data['sma50']:.4f}\n"

            f"📈 EMA20: "
            f"{data['ema20']:.4f}\n"

            f"📉 RSI: "
            f"{data['rsi']:.2f}\n"

            f"🌊 Волатильность: "
            f"{data['volatility']:.2f}%\n"

            f"📦 Volume ratio: "
            f"{data['volume_ratio']:.2f}x\n\n"

            f"📈 Тренд: "
            f"{data['trend']}\n"

            f"⚠️ Аномальность: "
            f"{data['anomaly_score']}/100"
        )

        await send_long_message(
            message,
            text
        )

        await message.answer(
            "🤖 Формирую AI-анализ..."
        )

        ai_result = analyze_market(
            data
        )

        await send_long_message(
            message,
            ai_result
        )

    except Exception as error:

        print(
            "SCAN ERROR:",
            repr(error)
        )

        await message.answer(
            "⚠️ Не удалось получить данные.\n\n"
            "Проверьте тикер и попробуйте ещё раз."
        )


# ============================================================
# TEXT
# ============================================================

@dp.message(
    F.text
)
async def text_handler(message: Message):

    text = message.text.strip()

    # --------------------------------------------------------
    # КНОПКИ
    # --------------------------------------------------------

    buttons = [
        "📊 Анализ актива",
        "🤖 AI-вопрос",
        "🔍 Проверить BTC",
        "🔍 Проверить ETH",
        "🧮 Калькулятор",
        "🌐 Актуальный поиск",
        "ℹ️ Помощь"
    ]

    if text in buttons:
        return

    # --------------------------------------------------------
    # ТИКЕР
    # --------------------------------------------------------

    clean = (
        text.upper()
        .replace("/", "")
        .replace("-", "")
    )

    if (
        len(clean) <= 10
        and clean.isalpha()
        and clean not in [
            "ПРИВЕТ",
            "ПОМОЩЬ"
        ]
    ):

        try:

            await scan_asset(
                message,
                clean
            )

            return

        except Exception:
            pass

    # --------------------------------------------------------
    # AI / CALCULATOR / SEARCH
    # --------------------------------------------------------

    await message.answer(
        "🤖 Анализирую запрос..."
    )

    result = ask_ai(text)

    await send_long_message(
        message,
        result
    )


# ============================================================
# MAIN
# ============================================================

async def main():

    print(
        "🛡️ FinGuard AI запущен!"
    )

    await dp.start_polling(
        bot
    )


if __name__ == "__main__":

    asyncio.run(main())