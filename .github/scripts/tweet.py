import os
import sys
from pathlib import Path
from urllib.parse import quote

import tweepy


def getenvs():
    return {"consumer_key": os.environ["TWITTER_CONSUMER_API_KEY"],
            "consumer_secret": os.environ["TWITTER_CONSUMER_API_SECRET"],
            "access_token": os.environ["TWITTER_ACCESS_TOKEN"],
            "access_token_secret": os.environ["TWITTER_ACCESS_TOKEN_SECRET"]}


def main():
    files = sys.argv[1:]
    if not files:
        print("No new files")
        return

    print(f"{len(files)} new articles were created")

    baseurl = os.environ["PAGE_URL"].rstrip("/")
    client = tweepy.Client(**getenvs())
    for file in files:
        p = Path(file).relative_to(".")
        client.create_tweet(
            text=f"New article has arrived! {baseurl}/{quote(str(p))}")


if __name__ == "__main__":
    exit(main())
