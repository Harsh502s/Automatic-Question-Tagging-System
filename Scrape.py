import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import lxml

df = pd.read_csv("50k.csv")
ques_head = []
ques_body = []
ques_tags = []
first_answer = []


def scrape(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "lxml")
        try:
            ques_h = soup.find("div", attrs={"id": "question-header"}).find("a").text
            ques_head.append(ques_h)
        except:
            ques_h = np.nan
            ques_head.append(ques_h)
            pass

        try:
            ques_b = soup.find("div", attrs={"class": "s-prose js-post-body"}).text
            ques_body.append(ques_b)
        except:
            ques_b = np.nan
            ques_body.append(ques_b)
            pass
        try:
            ques_t = soup.find("div", class_="d-flex ps-relative fw-wrap").find_all(
                "li", class_="d-inline mr4 js-post-tag-list-item"
            )
            ques_t = [tag.find("a").text for tag in ques_t]
            ques_tags.append(ques_t)
        except:
            ques_t = np.nan
            ques_tags.append(ques_t)
            pass
        try:
            fa = (
                soup.find("div", {"id": "answers"})
                .find(
                    "div", class_="answer js-answer accepted-answer js-accepted-answer"
                )
                .find("div", class_="answercell post-layout--right")
                .find("div", class_="s-prose js-post-body")
                .find_all("p")
            )
            fa = "".join([ans.text for ans in fa])
            first_answer.append(fa)
        except:
            fa = np.nan
            first_answer.append(fa)
    except:
        pass


for i in tqdm(df["Question Links"][35000:35003]):
    scrape(i)
    time.sleep(0.4)
data = pd.DataFrame(
    {
        "Head": ques_head,
        "Body": ques_body,
        "Tags": ques_tags,
        "First Answer": first_answer,
    }
)