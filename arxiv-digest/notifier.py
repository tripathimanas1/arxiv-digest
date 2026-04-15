import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_telegram(text: str):
    """Send a message via Telegram bot."""
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    response = requests.post(TELEGRAM_API, json=payload, timeout=10)
    response.raise_for_status()


def format_digest(papers_with_summaries: list[dict]) -> list[str]:
    """
    Format digest as multiple Telegram messages (one per paper).
    Telegram has a 4096 char limit per message.
    """
    messages = []

    # Header message
    from datetime import date
    header = (
        f"<b>Daily AI Research Digest</b>\n"
        f"{date.today().strftime('%B %d, %Y')}\n"
        f"Top {len(papers_with_summaries)} papers for you today\n"
        f"{'─' * 30}"
    )
    messages.append(header)

    # One message per paper
    for i, item in enumerate(papers_with_summaries, 1):
        paper = item["paper"]
        summary = item["summary"]

        msg = (
            f"<b>{i}. {paper['title']}</b>\n"
            f"<i>{paper['authors']}</i> | {paper['published']}\n\n"
            f"{summary}\n\n"
            f"<a href='{paper['link']}'>Read on arXiv</a>"
        )
        messages.append(msg)

    return messages


def send_digest(papers_with_summaries: list[dict]):
    """Send full digest to Telegram."""
    messages = format_digest(papers_with_summaries)
    for msg in messages:
        send_telegram(msg)
    print(f"Sent {len(messages)} messages to Telegram.")
