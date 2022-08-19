import os
import sys
from pathlib import Path

import tweepy
import yaml


def getenvs():
    return {"consumer_key": os.environ["TWITTER_CONSUMER_API_KEY"],
            "consumer_secret": os.environ["TWITTER_CONSUMER_API_SECRET"],
            "access_token": os.environ["TWITTER_ACCESS_TOKEN"],
            "access_token_secret": os.environ["TWITTER_ACCESS_TOKEN_SECRET"]}


def geturl():
    with open("_config.yml") as f:
        return yaml.safe_load(f)["url"]


def main():
    files = sys.argv[1:]
    if not files:
        print("No new files")
        return

    url = geturl()
    client = tweepy.Client(**getenvs())
    for file in files:
        p = Path(file).relative_to(".")
        client.create_tweet(text=f"New article has arrived! {url}/{p}")


if __name__ == "__main__":
    exit(main())
