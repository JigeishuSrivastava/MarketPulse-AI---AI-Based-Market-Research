import requests
from bs4 import BeautifulSoup

def scrape(url):

    try:

        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script","style"]):
            tag.decompose()

        text = soup.get_text()

        return text[:8000]

    except:

        return ""