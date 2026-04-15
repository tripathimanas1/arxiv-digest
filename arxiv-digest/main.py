import argparse
from fetcher import fetch_all_papers
from summarizer import summarize_paper, pick_top_papers
from notifier import send_digest

def run(dry_run: bool = False):
    print("Fetching papers from arXiv...")
    papers = fetch_all_papers()
    print(f"Found {len(papers)} papers total.")

    print("Picking top 5 most relevant...")
    top_papers = pick_top_papers(papers, n=5)
    print(f"Selected {len(top_papers)} papers.")

    papers_with_summaries = []
    for i, paper in enumerate(top_papers, 1):
        print(f"Summarizing {i}/{len(top_papers)}: {paper['title'][:60]}...")
        summary = summarize_paper(paper)
        papers_with_summaries.append({"paper": paper, "summary": summary})

    if dry_run:
        # Print to terminal instead of sending Telegram
        print("\n" + "="*60)
        print("DRY RUN — digest preview:")
        print("="*60)
        for item in papers_with_summaries:
            p = item["paper"]
            print(f"\n{p['title']}")
            print(f"{p['authors']} | {p['published']}")
            print(item["summary"])
            print(f"Link: {p['link']}")
            print("-"*40)
    else:
        print("Sending to Telegram...")
        send_digest(papers_with_summaries)
        print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print digest to terminal instead of sending Telegram"
    )
    args = parser.parse_args()
    run(dry_run=args.dry_run)
