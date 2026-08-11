import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не установлен! Добавь переменную окружения.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

PRODUCTS = {
    "capcut": {
        "name": "CapCut Pro",
        "price": "3000 ₸ / месяц\n17.000 ₸ / 6 месяцев"
    },
    "canva": {
        "name": "Canva Pro",
        "price": "5000 ₸ / 3 месяца"
    },
    "chatgpt": {
        "name": "ChatGPT Plus",
        "price": "10.000 ₸ / месяц"
    },
    "supergrok": {
        "name": "SuperGrok",
        "price": "10.000 ₸ / месяц"
    },
    "gemini": {
        "name": "Gemini Pro 18 месяцев",
        "price": "6000 ₸\n(гарантия 2 месяца)"
    },
    "office": {
        "name": "Microsoft Office",
        "price": "10.000 ₸ / 12 месяцев"
    }
}

def main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🎬 CapCut Pro", callback_data="product_capcut")],
        [InlineKeyboardButton(text="🎨 Canva Pro", callback_data="product_canva")],
        [InlineKeyboardButton(text="🤖 ChatGPT Plus", callback_data="product_chatgpt")],
        [InlineKeyboardButton(text="⚡ SuperGrok", callback_data="product_supergrok")],
        [InlineKeyboardButton(text="✨ Gemini Pro 18 мес.", callback_data="product_gemini")],
        [InlineKeyboardButton(text="📊 Microsoft Office", callback_data="product_office")],
        [InlineKeyboardButton(text="💬 Написать продавцу", url="https://t.me/qazmaker")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def payment_keyboard(product_key: str):
    buttons = [
        [InlineKeyboardButton(text="✅ Я оплатил(а)", callback_data=f"paid_{product_key}")],
        [InlineKeyboardButton(text="💬 Написать продавцу", url="https://t.me/qazmaker")],
        [InlineKeyboardButton(text="◀️ Назад к прайсу", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    text = (
        "💼 <b>Актуальный прайс на подписки</b>\n\n"
        "Выберите нужную подписку:\n\n"
        "Цены могут меняться время от времени.\n"
        "Принимаем: ₸  ₽  $  сом"
    )
    await message.answer(text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)

@dp.callback_query(F.data.startswith("product_"))
async def show_product(callback: CallbackQuery):
    product_key = callback.data.replace("product_", "")
    product = PRODUCTS.get(product_key)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    text = (
        f"<b>{product['name']}</b>\n\n"
        f"💰 Цена:\n{product['price']}\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"<b>Реквизиты для оплаты:</b>\n\n"
        f"Kaspi: <code>+77479683788</code>\n"
        f"Имя: Олег\n\n"
        f"После оплаты нажмите кнопку «Я оплатил(а)»\n"
        f"или напишите продавцу с чеком."
    )

    await callback.message.edit_text(
        text,
        reply_markup=payment_keyboard(product_key),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    text = (
        "💼 <b>Актуальный прайс на подписки</b>\n\n"
        "Выберите нужную подписку:\n\n"
        "Цены могут меняться время от времени.\n"
        "Принимаем: ₸  ₽  $  сом"
    )
    await callback.message.edit_text(
        text,
        reply_markup=main_keyboard(),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("paid_"))
async def paid_handler(callback: CallbackQuery):
    product_key = callback.data.replace("paid_", "")
    product = PRODUCTS.get(product_key, {"name": "Подписка"})

    await callback.message.edit_text(
        f"Спасибо! Вы выбрали: <b>{product['name']}</b>\n\n"
        f"Пожалуйста, отправьте чек об оплате продавцу:\n"
        f"👉 @qazmaker\n\n"
        f"После проверки чека подписка будет активирована.",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💬 Написать продавцу", url="https://t.me/qazmaker")],
            [InlineKeyboardButton(text="◀️ Вернуться к прайсу", callback_data="back_to_menu")]
        ])
    )
    await callback.answer("Отлично! Теперь отправьте чек продавцу.")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
