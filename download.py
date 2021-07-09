import json
import os.path
import requests
from time import sleep, perf_counter
from bs4 import BeautifulSoup

"""js
// Urls can be found by copying the output of this script on this page
// https://rosettacode.org/wiki/Category:Python

list = [];
document.querySelectorAll("#mw-pages a").forEach(e => {
    list.push(e.href)
    })
    a = {"list" : list}
}
"""

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
    name = f"downloads/{url.replace('/', '-')}.txt"

    if (os.path.isfile(name)):
        return

    print("Sleeping...")
    sleep(2) # don't abuse the server

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

    f = open(name, "w")
    f.write(result)
    f.close()

class Avg:
    def __init__(self):
        self.limit = 10
        self.times = []
        self.index = 0

    def add(self, num):
        self.index += 1

        if self.index >= self.limit:
            self.index = 0

        if self.index >= len(self.times):
            self.times.append(num)
        else:
            self.times[self.index] = num

    def getAvg(self):
        return sum(self.times) / len(self.times)

if __name__ == "__main__":
    avg = Avg()
    for i, url in enumerate(urls):
        start = perf_counter()
        save(url)
        stop = perf_counter()
        avg.add(stop - start)
        time_left = avg.getAvg() * (len(urls) - i + 1)
        print(f"\tTime left: {(time_left) / 60:.2f} minutes")

