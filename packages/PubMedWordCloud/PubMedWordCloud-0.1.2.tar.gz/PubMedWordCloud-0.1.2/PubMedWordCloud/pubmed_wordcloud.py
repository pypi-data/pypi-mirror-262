from Bio import Entrez
from datetime import datetime
from collections import Counter
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
import random
import os
import re
import nltk
import argparse

class PubMedWordCloud:
    def __init__(self, stopwords_list=None):
        if stopwords_list is None:
            nltk.download("stopwords")
            self.stopwords = stopwords.words("english")
        else:
            self.stopwords = stopwords_list

    def fetch_pubmed_titles(self, search_term, n_papers=10):
        Entrez.email = 'rahmani.biotech@gmail.com' 
        current_year = datetime.now().year
        start_date = f"{current_year - 1}"
        end_date = f"{current_year}"

        query = f'({search_term}) AND ("{start_date}"[Date - Publication] : "{end_date}"[Date - Publication])'

        handle = Entrez.esearch(db="pubmed", term=query, retmax=n_papers)
        record = Entrez.read(handle)
        handle.close()

        id_list = record["IdList"]
        titles = []

        for pubmed_id in id_list:
            handle = Entrez.efetch(db="pubmed", id=pubmed_id, retmode="xml")
            record = Entrez.read(handle)
            handle.close()
            title = record["PubmedArticle"][0]["MedlineCitation"]["Article"]["ArticleTitle"]
            titles.append(title)

        return titles

    def mine_words_from_titles(self, titles, Freq, length):
        matching_titles = []
        for title in titles:
            cleaned_title = re.sub(r"<.*?>", "", title)
            cleaned_title = re.sub(r"\.|:|,|study|case|via|among|novel|role", "", cleaned_title)
            title_words = cleaned_title.lower().split()
            title_words = [word.rstrip(".") for word in title_words]
            title_words = [word for word in title_words if len(word) >= length]
            matching_titles.append(title_words)
        word_counts = Counter(word for title_words in matching_titles for word in title_words)
        repeated_words = [word for word, count in word_counts.items() if count > Freq]
        text = " ".join(repeated_words)
        return text

    def generate_word_cloud(self, text, mask_image_path, figsize=(10, 10), color_func=None):
        mask = np.array(Image.open(mask_image_path))

        def random_color(word, font_size, position, orientation, random_state=None, **kwargs):
            h = random.randint(0, 360)
            s = random.randint(60, 100)
            l = random.randint(40, 70)
            return f"hsl({h}, {s}%, {l}%)"

        wordcloud = WordCloud(
            background_color="rgba(255, 255, 255, 0)",
            mode="RGBA",
            mask=mask,
            color_func=random_color,
            random_state=42,
        ).generate(text)

        plt.figure(figsize=figsize)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.imshow(mask, cmap=plt.cm.gray, interpolation="bilinear", alpha=0.2)
        plt.axis("off")

        save_path = os.path.join(os.getcwd(), "wordcloud.png")
        plt.savefig(save_path, bbox_inches="tight", pad_inches=0)
        plt.close()

        print(f"Word cloud image saved: {save_path}")

    def generate_pubmed_word_cloud(self, search_term, mask_image_path, n_papers=10, Freq=2, length=5, figsize=(18, 18)):
        titles = self.fetch_pubmed_titles(search_term, n_papers=n_papers)
        matching_titles = self.mine_words_from_titles(titles, Freq=Freq, length=length)
        self.generate_word_cloud(matching_titles, mask_image_path, figsize=figsize)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a word cloud from PubMed titles.")
    parser.add_argument("search_term", type=str, help="The search term for PubMed.")
    parser.add_argument("mask_image_path", type=str, help="The path to the mask image.")
    parser.add_argument("n_papers", type=int, help="The number of papers to search.")
    parser.add_argument("Freq", type=int, help="The frequency threshold.")
    parser.add_argument("length", type=int, help="The word length threshold.")
    parser.add_argument("figsize", type=str, help="The figure size (e.g., 18,18).")

    args = parser.parse_args()

    pubmed_word_cloud = PubMedWordCloud(stopwords_list="nltk_data")
    
    search_term = args.search_term
    mask_image_path = args.mask_image_path
    n_papers = args.n_papers
    Freq = args.Freq
    length = args.length
    figsize = tuple(map(int, args.figsize.split(',')))
    
    pubmed_word_cloud.generate_pubmed_word_cloud(
        search_term=search_term,
        mask_image_path=mask_image_path,
        n_papers=n_papers,
        Freq=Freq,
        length=length,
        figsize=figsize
    )

