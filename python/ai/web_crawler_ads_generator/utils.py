# web_crawler_ads_generator/utils.py

import argparse
from urllib.parse import urlparse


def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def parse_arguments():
    parser = argparse.ArgumentParser(description="Web crawler and ad generator")
    parser.add_argument("url", type=str, help="URL of the website to crawl")
    parser.add_argument("--max-pages", type=int, default=10, help="Maximum number of pages to crawl")
    parser.add_argument("--depth", type=int, default=3, help="Maximum depth for crawling")
    parser.add_argument("--ad-length", type=int, default=50, help="Maximum length of generated ads")
    parser.add_argument("--keywords", type=str, nargs='+', help="Keywords for ad generation")

    args = parser.parse_args()

    if not validate_url(args.url):
        raise ValueError("Invalid URL provided")

    return args
