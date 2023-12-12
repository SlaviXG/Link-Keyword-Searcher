from dataclasses import dataclass


@dataclass
class SearchResult:
    page_title: str
    page_link: str
    paragraph_text: str
