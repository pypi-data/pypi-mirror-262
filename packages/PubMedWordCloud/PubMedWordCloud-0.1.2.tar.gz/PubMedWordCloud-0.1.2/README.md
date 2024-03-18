**Generate a word cloud from PubMed titles.**

# Installation

```r{}
pip install PubMedWordCloud
```
# Running

```r{}
from PubMedWordCloud.pubmed_wordcloud import PubMedWordCloud
pubmed_word_cloud = PubMedWordCloud(stopwords_list="nltk_data")
pubmed_word_cloud.generate_pubmed_word_cloud(
    search_term="Interleukin-13 production",
    mask_image_path="dendritic_cell_mask.png",
    n_papers=100,
    Freq=2,
    length=5,
    figsize=(18, 18)
)

```

`search_term`` The search term for PubMed
`mask_image_path` The path to the mask image
`n_papers` The number of papers to search
`Freq` The frequency threshold
`length` The word length threshold
`figsize` The figure size (e.g., 18,18)
