from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def confirmation_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Да", callback_data="confirm")],
        [InlineKeyboardButton(text="Нет", callback_data="cancel")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
