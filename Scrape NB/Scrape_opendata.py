from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
import concurrent.futures as cf
import multiprocessing as mp

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
site = "https://opendata.stackexchange.com/questions?tab=newest&pagesize=50"
noofpages = None
response = requests.get(site)
soup = BeautifulSoup(response.text, "html.parser")
noofpages = int(
    soup.find("div", class_="s-pagination site498 themed pager float-left")
    .find_all("a")[-2]
    .text
)
urls = []
base_url = "https://opendata.stackexchange.com/questions?tab=newest&pagesize=50"
for i in range(1, int(noofpages) + 1):
    if i == 1:
        urls.append(base_url)
    else:
        urls.append(base_url + "&page=" + str(i))


def scrape():
    question_links = []
    for url in tqdm(urls):
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        for link in soup.find(
            "div", attrs={"class": "flush-left", "id": "questions"}
        ).find_all("a", attrs={"class": "s-link"}):
            question_links.append(
                "https://opendata.stackexchange.com" + link.get("href")
            )
    return pd.DataFrame(question_links, columns=["Question Links"])


df = scrape()
df.to_csv("question_links_opendata.csv", index=False)