from helper import get_tweet_df
import sys
import pandas as pd

qid = sys.argv[1]


df = get_tweet_df(qid)

title = df["itemLabel"][0]
doi = df["doi"][0]
tweet = f"""

I've just read "{title}" using Wikidata Bib!
https://doi.org/{doi}

"""

print(tweet)

for i, row in df.iterrows():
    tweet = tweet + f"""@{row["twitter_id"]} """


print()

tweet = (
    tweet
    + """
    
(prototype of auto-tweet generated using Wikidata)
"""
)

print(tweet)
