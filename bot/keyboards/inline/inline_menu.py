from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram import Router, F
from typing import Final

router: Final[Router] = Router(name="inline_menu")

# Обработчик нажатия на Inline кнопку
@router.callback_query(F.data == "show_instructions")
async def show_instructions(callback: CallbackQuery):
    instructions = (
        "<i>Инструкция по использованию:</i>\n\n"
        "1. Введите одну из команд\n"
        "2. В следующем сообщении введите ваш запрос\n\n"
        "<i>Запрос будет присылаться пока вы не переключите на другой режим работы "
        "(введете одну из других команд)</i>\n\n"
        "⚠️ <i>Примечание: после выполнения команды start история диалога внутри ИИ будет очищена!</i>"
    )

    await callback.message.answer(instructions, parse_mode=ParseMode.HTML)
    await callback.answer()
