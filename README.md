# Getting started

This is a tool which allows to search the information quickly in the multiple links.

- Install the necessary dependencies, run the following command:

`pip install -r requirements.txt`

- Download and install the correct version of the web driver:
  - [Chrome](https://sites.google.com/chromium.org/driver/downloads)
  - [Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

*It's important that the WebDriver version matches your browser version to ensure compatibility.*

- In this directory (if not created), create `keywords.txt` and `links.txt` files, and add the keywords and the links as
lines of th files according to the search you'd like to perform.
- Run the program with specifying the configuration:

`python search.py`
`python search.py --webdriver=chrome`

# Interface:

## Input:
List of keywords given in text file (by default: keywords.txt) among the links given in text file (by default: links.txt). 
The file paths can be specified via command line interface.

## Underneath:
- Read from the text fie all the links to search the information in.
- For each process consider the list of keywords and open a separate tab.
- In this tab, iterate through the list of keywords and save the matching search results.
- Return all the search results.
- Save all the search results to a separate file.

## Output:
Dictionary of the possible results, where key is a keyword and value is a list of the results.
The results are saved to a text file as well (by default: results.txt).


