from .helper import get_tweet_df
import pandas as pd
from pathlib import Path
import click

HERE = Path(__file__).parent.resolve()


@click.command(name="tweet")
def main():
    """
    Renders a tweet for the last read article.
    """
    read_path = HERE.parent.joinpath("data/read.csv").resolve()
    df = pd.read_csv(read_path)
    entries = list(df["wikidata_id"])
    qid = entries[-1]
    print(qid)

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

    if "twitter_id" in df.index:
        for i, row in df.iterrows():
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
