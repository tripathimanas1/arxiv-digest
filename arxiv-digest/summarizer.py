import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.0-flash"


def summarize_paper(paper: dict) -> str:
    """Return a 3-bullet summary of a paper, written for an AI engineer."""
    prompt = f"""
You are summarizing an AI research paper for a senior AI/ML engineer who builds LLM systems and red-teaming tools.

Paper title: {paper['title']}
Authors: {paper['authors']}
Abstract: {paper['summary']}

Give exactly 3 bullet points:
- What problem does it solve?
- What is the core method or finding?
- Why should an AI engineer working on LLM pipelines or safety care about this?

Be direct. No fluff. Each bullet max 2 sentences.
"""
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text.strip()


def pick_top_papers(papers: list[dict], n: int = 5) -> list[dict]:
    """Use Gemini to pick the most relevant papers from the full list."""
    if len(papers) <= n:
        return papers

    titles_list = "\n".join(
        f"{i+1}. {p['title']}" for i, p in enumerate(papers)
    )

    prompt = f"""
You are helping an AI engineer who works on LLM red-teaming, agentic systems, and LLM safety evaluation.

From this list of arXiv papers, pick the {n} most relevant and impactful ones.
Return only the numbers, comma-separated (e.g. 1,3,5,7,9).

Papers:
{titles_list}
"""
    response = client.models.generate_content(model=MODEL, contents=prompt)
    raw = response.text.strip()

    try:
        indices = [int(x.strip()) - 1 for x in raw.split(",") if x.strip().isdigit()]
        return [papers[i] for i in indices if i < len(papers)]
    except Exception:
        return papers[:n]
