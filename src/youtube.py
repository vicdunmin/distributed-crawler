from itertools import islice
from youtube_comment_downloader import *

import pandas as pd
import requests
import argparse


YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"
DEFAULT_TOP_COMMENT = 10
downloader = YoutubeCommentDownloader()


def get_trending_urls(num_urls=-1):
    response = requests.get(YOUTUBE_TRENDING_URL)
    html = response.text
    ids = set()
    urls = list()
    for i in range(len(html)):
        if html.startswith("videoId", i):
            # only add if it is alpha numeric
            if html[i + 10].isalnum():
                ids.add(html[i + 10 : i + 21])
    i = 0
    for id in ids:
        urls.append(f"https://youtube.com/watch?v={id}")
        if num_urls != -1: # default get all the trending urls else get specified number of urls
            i += 1
            if i >= num_urls:
                break
        
    return urls


def get_comments_from_url(url, top_comments):
    comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)
    cmt = []
    for comment in islice(comments, top_comments):
        cmt.append(comment["text"])
    return cmt[:top_comments]


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--top-comments",
        type=int,
        default=DEFAULT_TOP_COMMENT,
        help="Value of the variable in the top comments (default: %(default)s)",
    )
    args = parser.parse_args()

    # Set the value of the variable based on the command-line argument
    top_comments = args.top_comments

    comments_dict = {}
    trending_urls = get_trending_urls()
    for url in trending_urls:
        cmts = get_comments_from_url(url, top_comments)
        if len(cmts) < top_comments:
            continue
        comments_dict[url[-11:]] = cmts
        # only get 10 trending videos now
        if len(comments_dict) >= 10:
            break
    df = pd.DataFrame.from_dict(comments_dict)
    df.to_csv("trending_comments.csv")
