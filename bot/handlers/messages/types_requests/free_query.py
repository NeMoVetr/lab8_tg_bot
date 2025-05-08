from functools import lru_cache

from typing import Optional

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from langchain_core.chat_history import InMemoryChatMessageHistory

from langchain_core.runnables.history import RunnableWithMessageHistory

from bot.config.settings import get_settings

settings = get_settings()

# Загрузка настроек

# Инициализация LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=settings.openai.api_key)

# Промпт
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Вы - эксперт, готовый ответить на любой вопрос пользователя. Вместо MarkDown используй HTML разметку. Использовать только теги: b, i, u, s, a, code, pre. Другие теги использовать запрещено"),
    ("system", "Контекст (если есть): {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{query}")
])

# Основная цепочка
chain = prompt | llm | StrOutputParser()


# Функция для выдачи ИСТОРИИ сообщений по session_id
@lru_cache(maxsize=None)
def get_chat_history(session_id: str):
    """
    Возвращает историю сообщений для заданного session_id.
    :param session_id: идентификатор сессии
    :return: объект InMemoryChatMessageHistory
    """

    return InMemoryChatMessageHistory()


# Обёртка с памятью
chat_chain = RunnableWithMessageHistory(
    chain,
    get_session_history=get_chat_history,
    input_messages_key="query",
    history_messages_key="chat_history"
)


def answer_free_question(query: str, context: Optional[str] = None, session_id: str = "default") -> str:
    """
    Генерирует ответ на произвольный вопрос с учётом необязательного контекста.
    :param session_id: id сессии для загрузки из кэша истории сообщений
    :param query: текст вопроса
    :param context: дополнительный контекст для уточнения ответа
    :returns: сгенерированный ответ модели
    """

    context_value = context or ""
    return chat_chain.invoke(
        {"query": query, "context": context_value},
        config={"configurable": {"session_id": session_id}}
    )
