# Getting started

This is a tool which allows to search the information quickly in the multiple links.

To install the necessary requirements, run the following command:

`pip install -r requirements.txt`

# Interface:

## Input:
List of keywords given via command line interface.

## Underneath:
- Read from the text fie all the links to search the information in.
- For each process consider the list of keywords and open a separate tab.
- In this tab, iterate through the list of keywords and save the matching search results.
- Return all the search results.
- Save all the search results to a separate file.

## Output:
Dictionary of the possible results, where key is a keyword and value is a dictionary of the results.
The results are saved to a text file as well.


