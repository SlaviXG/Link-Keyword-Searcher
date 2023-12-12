import argparse
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from search_result import SearchResult


def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = []
        for line in file.readlines():
            line_strip = line.strip()
            if line_strip != '':
                lines.append(line_strip)

        return lines


def search_keyword_in_page(driver, keyword):
    results = []
    try:
        keyword_lower = keyword.lower()
        xpath_expression = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'{keyword_lower}')]"
        elements = driver.find_elements(By.XPATH, xpath_expression)

        for element in elements:
            if element.text.strip() != '':
                results.append(SearchResult(
                    page_title=driver.title,
                    page_link=driver.current_url,
                    paragraph_text=element.text
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


def process_link(link, keywords, web_driver, driver_path):
    driver = initialize_driver(web_driver, driver_path)
    results = {}
    driver.get(link)
    driver.implicitly_wait(5)

    for keyword in keywords:
        results[keyword] = search_keyword_in_page(driver, keyword)

    driver.quit()
    return results


def run_keyword_searcher(links_file: str,
                         keywords_file: str,
                         results_file: str,
                         web_driver: str,
                         driver_path: str = None):

    links = read_file(links_file)
    keywords = read_file(keywords_file)

    num_processes = min(multiprocessing.cpu_count(), len(links))

    with multiprocessing.Pool(num_processes) as pool:
        results = pool.starmap(process_link, [(link, keywords, web_driver, driver_path) for link in links])

    all_results = {}
    for result in results:
        for keyword, keyword_results in result.items():
            if keyword not in all_results:
                all_results[keyword] = []
            all_results[keyword].extend(keyword_results)

    with open(results_file, 'w') as file:
        for keyword, results in all_results.items():
            file.write(f"Keyword: {keyword}\n")
            for result in results:
                file.write(f"Title: {result.page_title}, Link: {result.page_link}, Text: {result.paragraph_text}\n")
            file.write("\n")

    print(f"Search completed. Results saved to {results_file}")

    return all_results


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
