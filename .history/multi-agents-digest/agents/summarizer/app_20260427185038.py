import os
import logging
import time
import google.genai as genai
from google.genai import types
from google.api_core import exceptions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("Summarizer")

INPUT_FILE = "/data/ingested.txt"
OUTPUT_FILE = "/data/summary.txt"

# Set up Gemini API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY environment variable is not set")
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

SYSTEM_PROMPT = (
    "You are a helpful assistant that summarizes text content. "
    "Extract key bullet points. Each bullet should be one "
    "concise sentence capturing a core insight."
)

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def summarize(text, retries=MAX_RETRIES):
    """Call Gemini API with retry logic for rate limits."""
    for attempt in range(retries):
        try:
            response = model.generate_content(
                [SYSTEM_PROMPT, text[:30000]],
                config=types.GenerateContentConfig(
                    max_output_tokens=1000,
                    temperature=0.3,
                )
            )
            return response.text
        except exceptions.ResourceExhausted:
            wait = RETRY_DELAY * (attempt + 1)
            logger.warning(f"Rate limit hit. Retrying in {wait} seconds...")
            time.sleep(wait)
        except exceptions.GoogleAPIError as e:
            logger.error(f"API error: {e}")
            raise
        except Exception as e:
            if "rate" in str(e).lower():
                wait = RETRY_DELAY * (attempt + 1)
                logger.warning(f"Rate limit hit. Retrying in {wait} seconds...")
                time.sleep(wait)
            else:
                logger.error(f"Error during summarization: {e}")
                raise
    raise RuntimeError("Max retries exceeded for LLM API Call")

def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            raw_text = f.read()
        
        if not raw_text.strip():
            logger.warning("Empty input. Writing fallback summary.")
            summary = "No content to summarize."
        else:
            summary = summarize(raw_text)
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(summary)
            logger.info(f"Summary written to {OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        raise

if __name__ == "__main__":
    main()