# Daily AI Research Digest

Fetches the latest arXiv papers on LLM red-teaming, agentic systems, and LLM safety — summarizes them with Gemini — and sends a clean digest to your Telegram every morning.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in your keys in .env
```

### Get your keys

**Gemini API key:**
- Go to https://aistudio.google.com → Get API Key

**Telegram Bot:**
1. Open Telegram → search `@BotFather`
2. Send `/newbot` → follow prompts → copy the token
3. Start a chat with your new bot
4. Get your chat ID: visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` after sending the bot a message

## Usage

**Test it (no Telegram, prints to terminal):**
```bash
python main.py --dry-run
```

**Send to Telegram:**
```bash
python main.py
```

## Automate with Cron (runs every morning at 8 AM)

```bash
crontab -e
```

Add this line:
```
0 8 * * * cd /path/to/arxiv-digest && python main.py >> logs/digest.log 2>&1
```

## Customize topics

Edit the `QUERIES` list in `fetcher.py`:
```python
QUERIES = [
    "LLM red-teaming safety",
    "agentic AI systems",
    "large language model evaluation",
]
```
