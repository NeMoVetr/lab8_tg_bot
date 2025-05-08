from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class CommandMainMenu:
    """
    Класс для создания команд главного меню бота.
    """

    __WEB: str
    __DOCS: str
    __ASK: str
    __RAG: str

    def __init__(self):
        """
        Инициализация команд главного меню.
        """

        self.__WEB = "🔍 Поиск в интернете (/search_web)"
        self.__DOCS = "📚 Поиск в документах (/search_docs)"
        self.__ASK = "❓ Задать вопрос (/ask)"
        self.__RAG = "🤖 RAG-пайплайн (/rag)"

    def get_web(self):
        return self.__WEB

    def get_docs(self):
        return self.__DOCS

    def get_ask(self):
        return self.__ASK

    def get_rag(self):
        return self.__RAG


def get_main_menu() -> ReplyKeyboardMarkup:
    """
    Создает основное меню с кнопками для команд бота:
    - search_web
    - search_docs
    - ask
    - rag
    """

    # Добавляем кнопки в две строки по две
    web = KeyboardButton(text=CommandMainMenu().get_web())

    docs = KeyboardButton(text=CommandMainMenu().get_docs())

    ask = KeyboardButton(text=CommandMainMenu().get_ask())
    rag = KeyboardButton(text=CommandMainMenu().get_rag())

    button1 = [web, docs]
    button2 = [ask, rag]

    markup = ReplyKeyboardMarkup(
        keyboard=[button1, button2],
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    return markup
