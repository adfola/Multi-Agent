# Test Input Files for Multi-Agent Pipeline

This directory contains sample test files used to validate the multi-agent pipeline.

## Files:
- **article1.txt** - High priority content with urgent/critical keywords
- **article2.txt** - Standard content with mixed priority
- **run_test.sh** - Script to run the full pipeline
- **expected_output.md** - Expected output format from the formatter agent

## How to test:
1. Ensure Docker is running
2. Set your GEMINI_API_KEY environment variable
3. Run: `bash run_test.sh` (or use docker-compose directly)
4. Check `../multi-agents-digest/output/daily_digest.md` for results
