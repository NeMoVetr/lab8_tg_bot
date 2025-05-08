from .free_query import answer_free_question
from .internet_search import search_internet
from .vector_search import search_documents

import re


async def rag_answer(query: str) -> str:
    """
    RAG-пайплайн: сначала ищем в интернете, потом документы,
    затем передаём оба контекста модели.

    :param query: Пользовательский запрос
    :returns: ответ модели на основе объединённого контекста
    """

    # Поиск в интернете
    web_results = await search_internet(query)
    web_context = "\n".join(
        f"{r['Источник']}: {r['Результат поиска']} ({r['URL']})"
        for r in web_results
    )

    # Поиск в документах
    docs = search_documents(query)
    doc_context = "\n".join(d.page_content for d in docs)

    # Составляем объединённый контекст
    combined_context = (
        f"Интернет:\n{web_context}\n\n"
        f"Документы:\n{doc_context}"
    )

    # Получаем ответ и обновляем память внутри free_query.chain
    answer = answer_free_question(query=query, context=combined_context)

    # Убираем заголовки h1-h6
    html = re.sub(r'<h[1-6]>(.*?)</h[1-6]>', r'<b>\1</b>', answer, flags=re.DOTALL)
    # Списки: заменяем <li>…</li> на • …\n и убираем теги <ul>, </ul>
    html = re.sub(r'<ul>|</ul>', '', html)
    html = re.sub(r'<li>(.*?)</li>', r'• \1\n', html, flags=re.DOTALL)
    # Параграфы: заменяем <p>…</p> на …\n
    html = re.sub(r'<p>(.*?)</p>', r'\1\n', html, flags=re.DOTALL)
    # Удаляем все остальные неподдерживаемые теги
    html = re.sub(r'<[^>]+>', '', html)

    return html
