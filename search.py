import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from search_result import SearchResult


def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


def search_keyword_in_page(driver, keyword):
    results = []
    try:
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        for paragraph in paragraphs:
            if keyword.lower() in paragraph.text.lower():
                results.append(SearchResult(
                    page_title=driver.title,
                    page_link=driver.current_url,
                    paragraph_text=paragraph.text
                ))
    except Exception as e:
        print(f"Error searching keyword '{keyword}' in page: {e}")
    return results


def initialize_driver(web_driver, driver_path):
    if web_driver == 'chrome':
        if driver_path:
            return webdriver.Chrome(executable_path=driver_path)
        return webdriver.Chrome()
    elif web_driver == 'edge':
        if driver_path:
            return webdriver.Edge(executable_path=driver_path)
        return webdriver.Edge()
    else:
        raise ValueError("Unsupported web driver specified")


def run_keyword_searcher(links_file: str, keywords_file: str, results_file: str, web_driver: str, driver_path: str = None):
    links = read_file(links_file)
    keywords = read_file(keywords_file)

    driver = initialize_driver(web_driver, driver_path)

    all_results = {}
    for link in links:
        driver.get(link)
        driver.implicitly_wait(5)  # Adjust based on page load time

        for keyword in keywords:
            if keyword not in all_results:
                all_results[keyword] = []
            all_results[keyword].extend(search_keyword_in_page(driver, keyword))

    driver.quit()

    with open(results_file, 'w') as file:
        for keyword, results in all_results.items():
            file.write(f"Keyword: {keyword}\n")
            for result in results:
                file.write(f"Title: {result.page_title}, Link: {result.page_link}, Text: {result.paragraph_text}\n")
            file.write("\n")

    print(f"Search completed. Results saved to {results_file}")


def main():
    parser = argparse.ArgumentParser(description="Run keyword Searcher")
    parser.add_argument('--links', help='File to read links from', default='links.txt', type=str, dest='links')
    parser.add_argument('--keywords', help='File to get keywords.txt from', default='keywords.txt', type=str, dest='keywords')
    parser.add_argument('--results', help='File to save the search results to', default='results.txt', type=str, dest='results')
    parser.add_argument('--webdriver', help='Web driver to perform the search in', default='edge', choices=['chrome', 'edge'], dest='web_driver')
    parser.add_argument('--driver-path', help='Specifying web driver path', required=False, dest='driver_path')

    args = parser.parse_args()
    run_keyword_searcher(links_file=args.links,
                         keywords_file=args.keywords,
                         results_file=args.results,
                         web_driver=args.web_driver,
                         driver_path=args.driver_path)


if __name__ == "__main__":
    main()
