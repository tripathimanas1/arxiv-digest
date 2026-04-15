import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

ARXIV_API = "http://export.arxiv.org/api/query"

# Topics relevant to your work — edit freely
QUERIES = [
    "LLM red-teaming safety",
    "agentic AI systems",
    "large language model evaluation",
]

MAX_RESULTS_PER_QUERY = 3


def fetch_papers(query: str) -> list[dict]:
    """Fetch recent papers from arXiv for a given query."""
    params = {
        "search_query": f"all:{query}",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": MAX_RESULTS_PER_QUERY,
    }

    response = requests.get(ARXIV_API, params=params, timeout=15)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    papers = []
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
        summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
        link = entry.find("atom:id", ns).text.strip()
        published = entry.find("atom:published", ns).text.strip()[:10]

        authors = [
            a.find("atom:name", ns).text
            for a in entry.findall("atom:author", ns)
        ]
        author_str = ", ".join(authors[:3])
        if len(authors) > 3:
            author_str += " et al."

        papers.append({
            "title": title,
            "summary": summary[:800],
            "link": link,
            "published": published,
            "authors": author_str,
            "query": query,
        })

    return papers


def fetch_all_papers() -> list[dict]:
    """Fetch papers for all configured topics, deduplicated."""
    seen_links = set()
    all_papers = []

    for query in QUERIES:
        papers = fetch_papers(query)
        for p in papers:
            if p["link"] not in seen_links:
                seen_links.add(p["link"])
                all_papers.append(p)

    return all_papers
