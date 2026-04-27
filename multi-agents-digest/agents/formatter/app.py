import os
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
# Set up logger for Formatter agent
logger = logging.getLogger("formatter")

INPUT_FILE = "/data/prioritized.txt"
OUTPUT_FILE = "/output/daily_digest.md"

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# format to markdown with bullet points and sections
def format_to_markdown():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
            out.write("# Your DAILY AI Digest\n\n")
            out.write(f"**Date:** {today}\n\n")
            out.write("## Top Insights\n\n")
            
            if not lines:
                out.write("No content to display.\n")
            else:
                for line in lines:
                    if ']' in line:
                        score = line.split(']')[0][1:]
                        content = line.split(']', 1)[1]
                        out.write(f"- {content} (Priority: {score})\n")
                    else:
                        out.write(f"- {line}\n")
        logger.info(f"Formatted digest with {len(lines)} items -> {OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"Error formatting digest: {e}")
        raise

if __name__ == "__main__":
    format_to_markdown()