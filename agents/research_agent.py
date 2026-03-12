from tools.search_tool import search_web
from tools.scraper import scrape
from memory.vector_store import store_data

def collect_data(queries):

    text_data = ""

    for q in queries:

        links = search_web(q)

        for link in links:

            text = scrape(link)

            text_data += text

            store_data(text)

    return text_data