# **Development Notes:**

```bash
cd /Users/macbookpro/GitHub/job-application-agentic-workflow
./run.sh setup              # Create venv + install deps
./run.sh install-browser    # Install Playwright Chromium
./run.sh verify             # Check Ollama models
./run.sh search             # Search LinkedIn + score jobs (no apply)
./run.sh run                # Full pipeline: search → match → apply
./run.sh mcp-server         # Start MCP browser automation server
```
