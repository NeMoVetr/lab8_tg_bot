from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import LanceDB
import lancedb
from langchain_openai import OpenAIEmbeddings

from bot.config.settings import get_settings

settings = get_settings()


# Настраиваем векторное хранилище
embeddings = OpenAIEmbeddings()
db = lancedb.connect(settings.vector_db.path)
table = db.open_table("pdf_docs")

# Создаём LangChain-обёртку
vector_store = LanceDB(
    connection=db,
    table_name="pdf_docs",
    embedding=embeddings
)

# Исправленный шаблон промпта
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    Вы помощник-ассистент, который отвечает на вопросы по содержимому документов.
    Используйте только информацию из блока контекста ниже:
    {context}

    Ответ должен включать:
    - Краткое резюме ответа
    - Список ключевых пунктов

    Ответ должен быть краток и содержать только факты из контекста.
    Вопрос: {question}
    """
)

# Создаём цепочку с исправленными параметрами
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.0),
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}), # 3 самых релевантных чанка из всех документов
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt}
)

# Функция-обёртка для запроса
def search_documents(query: str) -> str:
    doc = vector_store.similarity_search(query, k=3) # Выполняем поиск по векторному хранилищу, для проверки на наличие релевантных документов по вопросу
    return qa_chain.run(query) if doc else "Извините, ничего не найдено."