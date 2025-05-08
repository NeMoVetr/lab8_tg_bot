from typing import List, Dict

from langchain_community.tools import TavilySearchResults

from asyncio import to_thread

from bot.config.settings import get_settings

settings = get_settings()

# Инициализация инструмента поиска в интернете
search_tool = TavilySearchResults(max_results=3, tavily_api_key=settings.tevily.api_key)


async def search_internet(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Поиск информации в интернете с помощью TavilySearchResults из LangChain Community.

    :param query: поисковый запрос
    :param max_results: максимальное число результатов
    :returns: список результатов с полями title, url, content
    """

    # При необходимости изменить максимально возвращаемое число
    search_tool.max_results = max_results

    # Вызываем инструмент
    results = await to_thread(search_tool.invoke, query, None)

    # Оставляем только нужные поля
    formatted = []
    for r in results:
        formatted.append({
            "Источник": r.get("title"),
            "URL": r.get("url"),
            "Результат поиска": r.get("content") if r.get("content") else ''
        })
    return formatted
