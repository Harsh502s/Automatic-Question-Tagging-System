# Importing basic Libraries for EDA

import pandas as pd
import regex as re
from ast import literal_eval
import warnings

warnings.filterwarnings("ignore")


pd.set_option("display.max_columns", 10)

# Create a list of stopwords
import nltk
import spacy

stopwords_nltk = nltk.corpus.stopwords.words("english")
nlp = spacy.load("en_core_web_lg")
stopwords_spacy = nlp.Defaults.stop_words
stopwords = list(
    set(
        stopwords_nltk
        + list(stopwords_spacy)
        + list(stopwords_nltk)
        + list("abdefghijklmnopqstuvwxyz")
    )
)
print(len(stopwords))

df = pd.read_csv("Data/combined_df.csv")
df.head()

# Dropping the rows with missing values in the body and tags columns and dropping the duplicates.
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df["Text"] = df["Head"] + " " + df["Body"]

# Cleaning the tags
df["Tags Count"] = df["Tags"].apply(lambda x: len(literal_eval(x)))
df["Tags Count"] = df["Tags Count"].astype("int16")
df.info()

# Removing the rows with more than 5 tags
df = df[df["Tags Count"] <= 5]


def clean_text(text):
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.lower()
    text = text.strip()
    # Lemmatization and removing stopwords
    text = " ".join(
        [
            token.lemma_
            for token in nlp(text)
            if token.lemma_ not in stopwords and token.lemma_ != "-PRON-"
        ]
    )
    return text


df["Text"] = df["Text"].apply(clean_text)
df.head()
df.to_csv("Data/cleaned_data.csv", index=False)

## Now our data is in a good shape, we can start to do some analysis on it.
