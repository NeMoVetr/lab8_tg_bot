from typing import Final

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from asyncio import to_thread

from bot.keyboards.inline import get_main_menu, CommandMainMenu

from bot.handlers.messages.types_requests import answer_free_question, search_internet, search_documents, rag_answer

router: Final[Router] = Router(name=__name__)


class FormState(StatesGroup):
    """
    Состояния для обработки команд.
    """

    waiting_search_web = State() # Поиск в интернете
    waiting_search_docs = State() # Поиск в документах
    waiting_ask = State() # Свободный вопрос
    waiting_rag = State() # RAG-запрос


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """
    Обработчик команды /start.
    :param message: сообщение от пользователя
    :param state: контекст состояния
    :return: None
    """

    # Отправляем приветственное сообщение и очищаем состояние
    await state.clear()
    user = message.from_user.first_name

    # Создаем Inline кнопку с инструкцией
    instruction_button = InlineKeyboardButton(
        text="ℹ️ Инструкция по использованию",
        callback_data="show_instructions"
    )
    instruction_markup = InlineKeyboardMarkup(inline_keyboard=[[instruction_button]])

    html = (
        f"<b>Привет, {user}! 👋</b>\n\n"
        f"<i>Я – ваш финансовый ассистент. Вот мои команды:</i>\n\n"
        f"<b>1️⃣ /search_web</b> – Поиск в интернете\n"
        f"<b>2️⃣ /search_docs</b> – Поиск в документах\n"
        f"<b>3️⃣ /ask</b> – Свободный вопрос ИИ\n"
        f"<b>4️⃣ /rag</b> – RAG (интернет+доки+ИИ)\n\n"
    )
    await message.answer(html, reply_markup=get_main_menu(), parse_mode=ParseMode.HTML)
    await message.answer(
        "Нажмите кнопку ниже, чтобы увидеть инструкции по использованию:",
        reply_markup=instruction_markup
    )

# --- /search_web ---
@router.message(F.text == CommandMainMenu().get_web())
@router.message(Command("search_web"))
async def cmd_search_web(message: Message, state: FSMContext):
    """
    Обработчик команды /search_web.
    :param message:  сообщение от пользователя
    :param state:  контекст состояния
    :return:  None
    """

    # Сброс состояния и установка нового состояния
    await state.clear()
    await state.set_state(FormState.waiting_search_web)

    # Отправка сообщения с инструкцией
    html = "<i>Пожалуйста, введите текст для поиска в интернете:</i> <code>&lt;запрос&gt;</code>"
    await message.answer(html, parse_mode=ParseMode.HTML)


# --- /search_docs ---
@router.message(F.text == CommandMainMenu().get_docs())
@router.message(Command("search_docs"))
async def cmd_search_docs(message: Message, state: FSMContext):
    """
    Обработчик команды /search_docs.
    :param message:  сообщение от пользователя
    :param state:  контекст состояния
    :return:  None
    """

    # Сброс состояния и установка нового состояния
    await state.clear()
    await state.set_state(FormState.waiting_search_docs)

    # Отправка сообщения с инструкцией
    html = "<i>Пожалуйста, введите запрос для поиска в документах:</i> <code>&lt;запрос&gt;</code>"
    await message.answer(html, parse_mode=ParseMode.HTML)


# --- /ask ---
@router.message(F.text == CommandMainMenu().get_ask())
@router.message(Command("ask"))
async def cmd_ask(message: Message, state: FSMContext):
    """
    Обработчик команды /ask.
    :param message:  сообщение от пользователя
    :param state:  контекст состояния
    :return:  None
    """

    # Сброс состояния и установка нового состояния
    await state.clear()
    await state.set_state(FormState.waiting_ask)

    # Отправка сообщения с инструкцией
    html = "<i>Пожалуйста, введите ваш вопрос:</i> <code>&lt;вопрос&gt;</code>"
    await message.answer(html, parse_mode=ParseMode.HTML)


# --- /rag ---
@router.message(F.text == CommandMainMenu().get_rag())
@router.message(Command("rag"))
async def cmd_rag(message: Message, state: FSMContext):
    """
    Обработчик команды /rag.
    :param message: сообщение от пользователя
    :param state: контекст состояния
    :return: None
    """

    # Сброс состояния и установка нового состояния
    await state.clear()
    await state.set_state(FormState.waiting_rag)

    # Отправка сообщения с инструкцией
    html = "<i>Пожалуйста, введите запрос для RAG:</i> <code>&lt;запрос&gt;</code>"
    await message.answer(html, parse_mode=ParseMode.HTML)


# Обработчики состояний регистрируются после всех команд
@router.message(FormState.waiting_search_web)
async def process_search_web(message: Message, state: FSMContext):
    """
    Обработчик состояния ожидания поиска в интернете.
    :param state: контекст состояния
    :param message: сообщение от пользователя
    :return: None
    """

    # Получаем текст сообщения и удаляем лишние пробелы
    query = message.text.strip()
    if not query:
        await message.answer("<i>Нельзя отправить пустой запрос.</i>", parse_mode=ParseMode.HTML)
        return

    await message.answer(f"<b>🔍 Ищу в интернете:</b> {query}", parse_mode=ParseMode.HTML)

    # Выполняем поиск в интернете
    results = await search_internet(query)
    if not results:
        await message.answer("<i>Ничего не найдено.</i>", parse_mode=ParseMode.HTML)
    else:
        html_parts = []
        for r in results:
            html_parts.append(
                f"• <b>{r['Источник']}</b>: {r['Результат поиска']} "
                f"<a href=\"{r['URL']}\">Ссылка</a>"
            )
        await message.answer("\n".join(html_parts), parse_mode=ParseMode.HTML)

        # Сбрасываем состояние, НО сохраняем данные (историю)
        await state.set_state(None)


@router.message(FormState.waiting_search_docs)
async def process_search_docs(message: Message, state: FSMContext):
    """
    Обработчик состояния ожидания поиска в документах.
    :param state: контекст состояния
    :param message: сообщение от пользователя
    :return: None
    """

    # Получаем текст сообщения и удаляем лишние пробелы
    query = message.text.strip()
    if not query:
        await message.answer("<i>Нельзя отправить пустой запрос.</i>", parse_mode=ParseMode.HTML)
        return

    await message.answer(f"<b>📚 Ищу в документах:</b> {query}", parse_mode=ParseMode.HTML)

    # Выполняем поиск в документах
    docs = await to_thread(search_documents, query)
    if not docs:
        await message.answer("<i>Ничего не найдено.</i>", parse_mode=ParseMode.HTML)
    else:
        html_parts = []
        for d in docs:
            html_parts.append(d.page_content)
        await message.answer("\n\n".join(html_parts), parse_mode=ParseMode.HTML)

        # Сбрасываем состояние, НО сохраняем данные (историю)
        await state.set_state(None)


@router.message(FormState.waiting_ask)
async def process_ask(message: Message, state: FSMContext):
    """
    Обработчик состояния ожидания свободного вопроса.
    :param state: контекст состояния
    :param message: сообщение от пользователя
    :return: None
    """

    # Получаем текст сообщения и удаляем лишние пробелы
    query = message.text.strip()
    if not query:
        await message.answer("<i>Нельзя отправить пустой запрос.</i>", parse_mode=ParseMode.HTML)
        return

    # Получаем ID пользователя
    user_id = message.from_user.id

    await message.answer(f"<b>❓ Вопрос:</b> {query}", parse_mode=ParseMode.HTML)

    # Выполняем свободный вопрос
    answer = answer_free_question(query, session_id=str(user_id))

    await message.answer(answer, parse_mode=ParseMode.HTML)

    # Сбрасываем состояние, НО сохраняем данные (историю)
    await state.set_state(None)


@router.message(FormState.waiting_rag)
async def process_rag_query(message: Message, state: FSMContext):
    """
    Обработчик состояния ожидания RAG-запроса.
    :param state: контекст состояния
    :param message: сообщение от пользователя
    :return: None
    """

    # Получаем текст сообщения и удаляем лишние пробелы
    query = message.text.strip()
    if not query:
        await message.answer("<i>Нельзя отправить пустой запрос.</i>", parse_mode=ParseMode.HTML)
        return

    await message.answer(f"<b>🤖 RAG-запрос:</b> {query}", parse_mode=ParseMode.HTML)

    # Выполняем RAG-запрос
    md_answer = await rag_answer(query)

    await message.answer(md_answer, parse_mode=ParseMode.HTML)

    # Сбрасываем состояние, НО сохраняем данные (историю)
    await state.set_state(None)
