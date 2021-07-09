import json
import requests
from bs4 import BeautifulSoup

urls = []
with open("urls.json") as f:
    urls = json.load(f)["list"]

if urls == []:
    exit(1)

def download(url):
    print(f"downloading {url}...")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    for br in soup.find_all("br"):
        br.replace_with("\n")
    py_results = soup.find_all(class_="python")
    rb_results = soup.find_all(class_="ruby")
    return (py_results, rb_results)


def save(url):
    python, ruby = download(url)

    result = ""
    for r in ruby:
        result += "====RUBY=====\n"
        result += r.get_text()
        result += "\n\n"

    for p in python:
        result += "====PYTHON=====\n"
        result += p.get_text()
        result += "\n\n"

    f = open(f"downloads/{url.replace('/', '-')}.txt", "w")
    f.write(result)
    f.close()

if __name__ == "__main__":
    save(urls[0])
