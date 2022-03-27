from helper import get_tweet_df
import sys
import pandas as pd

import pandas as pd


if len(sys.argv) == 1:
    df = pd.read_csv("read.csv")
    entries = list(df["wikidata_id"])
    qid = entries[-1]
    print(qid)
else:
    qid = sys.argv[1]


df = get_tweet_df(qid)

if df.empty:
    print("No data available for building the tweet.")
    quit()

title = df["itemLabel"][0]
doi = df["doi"][0]
tweet = f"""

I've just read "{title}"
https://doi.org/{doi}

"""

for i, row in df.iterrows():
    tweet = tweet + f"""@{row["twitter_id"]} """


tweet = (
    tweet
    + """
    
(auto-tweet powered by Wikidata)
"""
)

print(tweet)
