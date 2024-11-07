import os
import telebot
from dotenv import load_dotenv

load_dotenv()
#API_KEY = "7681074358:AAG628qlzRpi0ofFy7wnVEzWMfqUviYyciw"

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["jokes"])
def send_jokes(message):
    bot.send_message(message.chat.id, "Here is a joke for you:")

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a stand up comedian"},
        {"role": "user", "content": "tell me a joke about IT guys"},
    ],)

    bot.send_message(
        message.chat.id, response.choices[0].message.content, parse_mode="Markdown"
    )

@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    # bot.(message, "Howdy, how are you doing?")
    bot.send_message(message.chat.id, "Howdy, how are you doing?")

@bot.message_handler(commands=["chelsea"])
def send_chelsea(message):
    bot.reply_to(message, "Chelsea is the best team in the world")
    bot.send_message(message.chat.id, "Chelsea is the best team in the world")


@bot.message_handler(commands=["chat"])
def send_chat(message):
    # bot.send_message(message.chat.id, "Chat with me")
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Introduce your self"},
        {"role": "user", "content": message.text},
    ],
    )

    bot.send_message(
        message.chat.id, response.choices[0].message.content, parse_mode="Markdown"
    )

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


@bot.message_handler(commands=["wiki"])
def send_wiki(message):
    import os

    bot.send_message(message.chat.id, "Here is the wiki for you:")

    wiki = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else ""
    )

    os.environ['OPENAI_API_KEY']='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'

    os.environ['USER_AGENT'] = 'myagent'

    os.environ["LANGCHAIN_API_KEY"] = "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"

    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o-mini")

    import bs4
    from langchain_community.document_loaders import WikipediaLoader
    from langchain import hub
    from langchain_chroma import Chroma
    from langchain_community.document_loaders import WebBaseLoader
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from langchain_openai import OpenAIEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # Load, chunk and index the contents of the blog.

    docs = WikipediaLoader(query="Olympics 2024", load_max_docs=2).load()

    len(docs)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    results = rag_chain.invoke(wiki)

    bot.send_message(
        message.chat.id, results, parse_mode="Markdown"
    )



@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
