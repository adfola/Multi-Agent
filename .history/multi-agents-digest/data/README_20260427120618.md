# Data Directory Structure

## Input Folder (`input/`)
Place your source documents here (`.txt`, `.md`, etc.)
The ingestor agent will read all files from this directory

## Intermediate Files (root)
- `ingested.txt` - Output from Ingestor agent (combined raw content)
- `summary.txt` - Output from Summarizer agent (key bullet points)
- `prioritized.txt` - Output from Prioritizer agent (ranked by importance)

## Output Folder (`../output/`)
- `daily_digest.md` - Final formatted markdown report

## Data Flow:
```
input/ 
  ↓ (Ingestor)
ingested.txt 
  ↓ (Summarizer - Gemini API)
summary.txt 
  ↓ (Prioritizer)
prioritized.txt 
  ↓ (Formatter)
../output/daily_digest.md
```
