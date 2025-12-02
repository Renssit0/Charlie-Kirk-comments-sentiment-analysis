# Charlie Kirk sentiment analysis

## Objective

Charlie Kirks' assasination has brought a lot of media attention from both supporters and critics, and as the political globe takes a look back at his legacy, some sour comments are bound to appear. As his figure has always been a controversial one, this might not be all too new, however bringing an end to a life is unjustifiable even for many of the most tenacious critics. Perhaps in this time for mourning, he won't be so viciously critiqued. Or perhaps the comments of the furthest extreme of the opposition will bring even more hate to the conversation. 

This project aims to uncover the answers to these questions by contrasting reddit comments before and after his death.

## Dataset

As previously stated, this dataset has been scrapped of Reddit using its API. The dataset can be found in [Hugging Face](https://huggingface.co/datasets/Renssit0/Charlie-Kirk-comments) and the code used can be found at "src/reddit_scrapper.py".


## Process

All code is located in "/src" and has a corresponding document in "/doc" that explains it in Spanish in natural language.

In order to reproduce the result, you may run the "/src/1-reddit_scrapper.py" to scrap results on your own or take our scrapped dataset from hugging face and download it into the data/raw directory, at which point you can run each notebook in "/src" in the following order: "2.1-data_cleaning.ipynb", "2.2-metrics.ipynb" and "3-visualization/visualization.ipynb".

The dataset from raw to fully processed goes through these filenames:
> comentarios_charlie_kirk_balanceado.csv -> charlie_kirk_comments_cleaned.csv -> charlie_kirk_comments_processed.csv

Finally, in visualization, we draw conclusions in the last notebook.

## License
This repository is licensed under:  
- [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)  

The dataset mentioned in this repo is licensed separately:  
- [Reddit API terms](https://redditinc.com/policies/data-api-terms)

