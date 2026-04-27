# Multi-Agent AI Digest Pipeline

## 📋 Overview

This is a containerized **multi-agent system** that processes documents into a daily AI digest using Google Gemini API. Four independent agents work in sequence:

1. **Ingestor** - Combines all input files
2. **Summarizer** - Extracts key points using Gemini AI
3. **Prioritizer** - Ranks content by importance keywords
4. **Formatter** - Generates markdown report

---

## 🔄 How It Works

### Pipeline Flow:
```
📁 input/ files 
    ↓
[Ingestor Agent]
    ↓ (ingested.txt - raw combined content)
[Summarizer Agent] (uses Google Gemini API)
    ↓ (summary.txt - bullet points)
[Prioritizer Agent]
    ↓ (prioritized.txt - scored by keywords)
[Formatter Agent]
    ↓ (daily_digest.md - final markdown report)
📁 output/
```

---

## 🛠️ Agent Details

### 1. **Ingestor** (`agents/ingestor/`)
**What it does:** Reads all files from `/data/input/` and merges them into a single file
- **Input:** Multiple files in `/data/input/`
- **Output:** `/data/ingested.txt`
- **Dependencies:** None (pure Python)
- **Process:** 
  - Reads files alphabetically
  - Adds file headers for tracking
  - Handles encoding errors gracefully

### 2. **Summarizer** (`agents/summarizer/`)
**What it does:** Uses Google Gemini API to extract key bullet points
- **Input:** `/data/ingested.txt`
- **Output:** `/data/summary.txt`
- **Dependencies:** `google-generativeai>=0.3.0`
- **Process:**
  - Sends content to Gemini 1.5 Pro model
  - Extracts concise insights
  - Has retry logic for rate limits
  - Truncates input to 30K tokens to avoid limits

### 3. **Prioritizer** (`agents/prioritizer/`)
**What it does:** Ranks lines by presence of priority keywords
- **Input:** `/data/summary.txt`
- **Output:** `/data/prioritized.txt`
- **Dependencies:** None
- **Priority Keywords:** urgent, today, asap, important, deadline, critical, action required
- **Output Format:** `[score] content` where score is keyword count

### 4. **Formatter** (`agents/formatter/`)
**What it does:** Converts prioritized content into a polished markdown report
- **Input:** `/data/prioritized.txt`
- **Output:** `/output/daily_digest.md`
- **Dependencies:** None
- **Features:**
  - Adds date stamp
  - Creates "Top Insights" section
  - Preserves priority scores
  - Professional markdown formatting

---

## 🚀 Quick Start

### Prerequisites:
- Docker & Docker Compose installed
- Google Gemini API key (free tier available at https://ai.google.dev)

### Setup:

1. **Set your API key:**
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```

2. **Add input files** to `multi-agents-digest/data/input/`:
   ```bash
   cp your_document.txt multi-agents-digest/data/input/
   ```

3. **Run the pipeline:**
   ```bash
   docker-compose up
   ```

4. **Check output:**
   ```bash
   cat multi-agents-digest/output/daily_digest.md
   ```

---

## 📁 Directory Structure

```
.
├── docker-compose.yml          # Orchestrates all 4 agents
├── README.md                   # This file
├── multi-agents-digest/
│   ├── agents/
│   │   ├── ingestor/
│   │   │   ├── app.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt (empty)
│   │   ├── summarizer/
│   │   │   ├── app.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt (google-generativeai)
│   │   ├── prioritizer/
│   │   │   ├── app.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt (empty)
│   │   └── formatter/
│   │       ├── app.py
│   │       ├── Dockerfile
│   │       └── requirements.txt (empty)
│   ├── data/
│   │   ├── input/              # Place your documents here
│   │   ├── ingested.txt        # Auto-generated
│   │   ├── summary.txt         # Auto-generated
│   │   ├── prioritized.txt     # Auto-generated
│   │   └── README.md
│   └── output/
│       └── daily_digest.md     # Final output
└── test/
    ├── run_test.sh             # Test script
    ├── expected_output.md      # Reference output
    ├── README.md
```

---

## 🐛 Bugs Fixed

### Code Issues Resolved:
✅ **Ingestor**: Undefined `files_processed` variable, broken exception handling  
✅ **Summarizer**: Indentation errors, misplaced file write logic  
✅ **Prioritizer**: Unused imports, logging in loop, wrong indentation  
✅ **Formatter**: Missing `datetime` import, wrong output path  

### Dockerfile Issues Fixed:
✅ Fixed `FROM python: 3.10-slim` → `FROM python:3.10-slim` (spaces removed)  
✅ Created missing Formatter Dockerfile  
✅ Updated Summarizer requirements to `google-generativeai>=0.3.0`  

---

## 📊 Sample Input/Output

### Input (article1.txt):
```
This is a critical update about urgent security patching. 
Action required: All systems must be updated today.
This is an ASAP priority item with an important deadline.
```

### Output (daily_digest.md):
```markdown
# Your DAILY AI Digest

**Date:** 2024-01-15

## Top Insights

- All systems must be updated today (Priority: 3)
- Critical security update needed (Priority: 2)
```

---

## ⚙️ Configuration

### Environment Variables:
- `GEMINI_API_KEY` - Required for Summarizer agent
- `PYTHONUNBUFFERED=1` - Docker logging (pre-configured)

### Customizing Priority Keywords:
Edit `agents/prioritizer/app.py`:
```python
PRIORITY_KEYWORDS = [
    "urgent", "today", "asap", "important",
    "deadline", "critical", "action required"
]
```

---

## 🔧 Troubleshooting

### Issue: "GEMINI_API_KEY not set"
**Solution:** Export your API key before running:
```bash
export GEMINI_API_KEY="your-key"
docker-compose up
```

### Issue: "No input files found"
**Solution:** Place files in `multi-agents-digest/data/input/` and ensure they're readable

### Issue: "Rate limit exceeded"
**Solution:** Summarizer automatically retries. Wait a moment and rerun.

---

## 📝 License
MIT
