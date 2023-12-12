import argparse


def run_keyword_searcher(links_file: str,
                         keywords_file: str,
                         results_file: str):
    print(links_file)
    print(keywords_file)
    print(results_file)


def main():
    parser = argparse.ArgumentParser(description="Run keyword Searcher")
    parser.add_argument('--links', help='File to read links from', default='links.txt', type=str, dest='links')
    parser.add_argument('--keywords', help='File to get keywords from', default='keywords.txt', type=str, dest='keywords')
    parser.add_argument('--results', help='File to save the search results to', default='results.txt', type=str, dest='results')

    args = parser.parse_args()

    run_keyword_searcher(links_file=args.links,
                         keywords_file=args.keywords,
                         results_file=args.results)


if __name__ == "__main__":
    main()
