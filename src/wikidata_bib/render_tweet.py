"""
Renders a basic tweet about the last read paper.
"""
import sys
from pathlib import Path

import click
import pandas as pd

from .helper import get_tweet_df

HERE = Path(__file__).parent.resolve()


@click.command(name="tweet")
def main():
    """
    Renders a tweet for the last read article.
    """
    read_path = HERE.parent.joinpath("data/read.csv").resolve()
    read_articles_dataframe = pd.read_csv(read_path)
    entries = list(read_articles_dataframe["wikidata_id"])
    qid = entries[-1]
    print(qid)

    tweet_dataframe = get_tweet_df(qid)

    if tweet_dataframe.empty:
        print("No data available for building the tweet.")
        sys.exit()

    title = tweet_dataframe["itemLabel"][0]
    doi = tweet_dataframe["doi"][0]
    tweet = f"""

  I've just read "{title}"
  https://doi.org/{doi}

  """

    if "twitter_id" in tweet_dataframe.index:
        for _, row in tweet_dataframe.iterrows():
            if row["twitter_id"] == row["twitter_id"]:  # Test for NaN
                tweet = tweet + f"""@{row["twitter_id"]} """

    tweet = (
        tweet
        + """

  (auto-tweet powered by Wikidata)
  """
    )

    print(tweet)


if __name__ == "__main__":
    main()
