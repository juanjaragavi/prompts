# Job Application Automation - Refactored Structure

This is a refactored, modular version of the job application automation system. It consolidates 20+ fragmented scripts into a clean, maintainable architecture.

## Architecture Overview

```
├── config.yaml                          # Centralized configuration (candidate, resumes, platforms, selectors)
├── config.py                            # Config loader and validator
├── job_application_bot.py               # Base bot class with common methods
├── apply_all_refactored.py              # Multi-platform bot (uses base class)
├── requirements.txt                     # Python dependencies
├── test_setup.py                        # Verify config and bot setup
├── open_applications_inventory_template.json  # Job inventory template
└── [logs/, screenshots/, application_status_*.json]  # Output directories (created at runtime)
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Update Configuration

Edit `config.yaml` with your details:

- Verify candidate data (name, email, phone, links)
- Verify resume file paths (must be absolute paths or relative to working directory)
- Review platform selectors (these are already configured for common platforms)

### 3. Create Job Inventory

Copy the template and add your job URLs:

```bash
cp open_applications_inventory_template.json open_applications_inventory.json
```

Edit `open_applications_inventory.json` and add your target jobs:

```json
[
  {
    "index": 1,
    "company": "Rappi",
    "job_title": "AI Engineer - Backend",
    "platform": "lever",
    "url": "https://jobs.lever.co/rappi/..."
  },
  {
    "index": 2,
    "company": "Provectus",
    "job_title": "Senior ML Engineer",
    "platform": "workable",
    "url": "https://provectus.workable.com/..."
  }
]
```

### 4. Test the Setup

```bash
python test_setup.py
```

Expected output:

```
✓ Config loaded successfully
✓ Candidate: Juan Miguel Jaramillo Gaviria
✓ Master resume path: ...
✓ Platforms configured: smartrecruiters, workable, lever, ashby, crelate, rippling, zoho_recruit
✓ All tests passed! Ready to run applications.
```

### 5. Run Applications

```bash
python apply_all_refactored.py
```

The bot will:

- Load each job from `open_applications_inventory.json`
- Route to platform-specific handler
- Fill forms automatically
- Upload resumes/documents
- Attempt submission
- Save status and screenshots to `application_status_*.json` and `screenshots/`
- Log everything to `logs/bot_YYYYMMDD_HHMMSS.log`

## Configuration Details

### config.yaml Structure

**candidate**: Personal data (name, email, phone, LinkedIn, GitHub, portfolio, compensation expectations)

**resumes**: Map resume variants to file paths

- `ai_llm`: For AI/ML-focused roles
- `vibe_coding`: For fast-paced development roles
- `master`: Default/fallback resume

**documents**: Supporting files (cover letter, certificates, screenshots)

**platforms**: For each job board, define:

- HTML form selectors (where to fill first_name, email, etc.)
- Default resume variant to use
- Custom questions (if any)

**output**: Directory paths for logs, screenshots, status files

**browser**: Playwright browser config (headless mode, viewport, timeouts, user-agent)

**essay_templates**: Pre-written responses for common essay questions

**anti_patterns**: Keywords that trigger blocking detection (Cloudflare, CAPTCHA, "access restricted")

### Platform Selectors

Selectors are CSS/XPath strings pointing to form fields. They're pre-configured for:

| Platform        | Support | Resume Upload    | Custom Questions         |
| --------------- | ------- | ---------------- | ------------------------ |
| SmartRecruiters | ✓       | Yes              | No                       |
| Workable        | ✓       | Yes              | Yes (10+)                |
| Lever           | ✓       | Yes              | No                       |
| Ashby           | ✓       | Yes              | Optional                 |
| Crelate         | ✓       | Yes              | No                       |
| Rippling        | ✓       | Yes              | Yes (salary, experience) |
| Zoho Recruit    | ✓       | Yes (multi-file) | Yes                      |

**To add a new platform:**

1. Add entry to `config.yaml` under `platforms:`
2. Add selector mappings (inspect the job form HTML)
3. Create handler method `_handle_<platform_name>()` in `MultiPlatformBot` class

## Output & Monitoring

### Logs

```
logs/bot_20250115_143022.log
```

Structured logs with DEBUG, INFO, WARNING, ERROR levels:

```
2025-01-15 14:30:22 - JobApplicationBot - INFO - Processing Index 1: Rappi - AI Engineer
2025-01-15 14:30:23 - JobApplicationBot - DEBUG - Loaded: https://...
2025-01-15 14:30:24 - JobApplicationBot - DEBUG - Filled first_name: input[name='firstname']
2025-01-15 14:30:25 - JobApplicationBot - INFO - Status saved: application_status_1.json - Submitted
```

### Status Files

```
application_status_1.json
```

JSON with full application details:

```json
{
  "index": 1,
  "company": "Rappi",
  "job_title": "AI Engineer",
  "platform": "lever",
  "url": "https://...",
  "status": "Submitted",
  "screenshot_path": "/path/to/screenshots/application_1_20250115_143025.png",
  "details": "Form submitted on Lever",
  "timestamp": "2025-01-15T14:30:25.123456"
}
```

**Status Values:**

- `Submitted` - Application successfully submitted
- `Form Filled` - Form filled but could not find submit button
- `Blocked by Anti-Bot` - Cloudflare/CAPTCHA detected
- `Requires Manual Action` - Platform not supported or form structure unknown
- `Failed to Load` - Could not access job page
- `Error` - Exception during processing
- `Unsupported Platform` - Platform not in config

### Screenshots

```
screenshots/
├── application_1_20250115_143025.png
├── application_2_20250115_143030.png
├── blocked_3_20250115_143035.png
└── error_4_20250115_143040.png
```

Screenshots help debug form-filling issues and capture proof of submission.

## Advanced Usage

### Run Single Platform Only

To test or run only one platform:

```python
# In apply_all_refactored.py, modify main():
for app in inventory:
    if app['platform'].lower() != 'lever':
        continue
    # ... rest of loop
```

### Custom Resume per Job

Edit `open_applications_inventory.json`:

```json
{
  "index": 1,
  "company": "Rappi",
  "job_title": "AI Engineer",
  "platform": "lever",
  "url": "https://...",
  "resume_variant": "ai_llm"  # Override default
}
```

Then in `apply_all_refactored.py`, modify platform handlers to read the override:

```python
resume_variant = app.get('resume_variant', platform_config["resume_variant"])
```

### Add New Platform

1. **Inspect the form** — open job page, right-click form fields, copy CSS selectors
2. **Update config.yaml**:
   ```yaml
   newplatform:
     name: 'New Platform'
     selectors:
       first_name: "input[id='fname']"
       email: "input[id='email']"
       # ... other fields
     resume_variant: 'master'
   ```
3. **Add handler in `apply_all_refactored.py`**:
   ```python
   async def _handle_newplatform(self, page, index) -> tuple:
       platform_config = self.config.get_platform_config("newplatform")
       selectors = platform_config["selectors"]
       # ... fill fields, upload resume, submit
       return "Submitted", "Form submitted on New Platform"
   ```
4. **Update router**:
   ```python
   elif platform_lower == "newplatform":
       status, details = await self._handle_newplatform(page, index)
   ```

### Headless Mode & Debugging

To see the browser in action (useful for debugging):

```python
bot = MultiPlatformBot(headless=False)  # Shows browser window
```

Or modify `config.yaml`:

```yaml
browser:
  headless: false
```

### Rate Limiting & Delays

Modify browser config in `config.yaml`:

```yaml
browser:
  action_wait_ms: 2000 # Wait 2s between actions (default 1s)
  page_load_wait_ms: 5000 # Wait 5s after page loads (default 5s)
```

To add delays between jobs, edit `apply_all_refactored.py`:

```python
for app in inventory:
    # ... process app
    await asyncio.sleep(30)  # Wait 30s between jobs
```

## Troubleshooting

### "Config file not found"

- Ensure `config.yaml` is in the same directory as `config.py`
- Check working directory: `python -c "import os; print(os.getcwd())"`

### "Resume file not found"

- Check paths in `config.yaml` are correct and absolute (or valid relative paths)
- On Mac: `/Users/macbookpro/...` (verify home directory)
- On Linux: `/home/username/...`
- On Windows: `C:\\Users\\username\\...`

### "Selector not found"

- The form structure may have changed
- Check screenshots to see what was rendered
- Update selectors in `config.yaml` with correct CSS selectors
- Use browser DevTools: right-click → Inspect → copy selector

### "Blocked by anti-bot"

- Some platforms use Cloudflare or CAPTCHA
- The bot detects this and returns `"Requires Manual Action"` status
- Manually submit these applications or use a proxy/VPN

### "Submit button not found"

- Form may require solving a CAPTCHA first
- Form may be incomplete (required fields missing)
- Check logs and screenshots to diagnose
- Update submit button selector in `config.yaml`

## Future Enhancements

Phase 2 (already sketched):

- [ ] Job Queue System: Track submitted, pending, failed states in SQLite
- [ ] Resumable Runs: If bot crashes, pick up where it left off
- [ ] Retry Logic: Exponential backoff for network timeouts

Phase 3:

- [ ] Docker containerization for consistent environments
- [ ] APScheduler for automated daily runs

Phase 4:

- [ ] HTML dashboard to view application stats
- [ ] CSV export for trending and analysis

## Support & Maintenance

**To update a platform's selectors:**

1. Open the job page manually
2. Inspect the form fields (DevTools → Elements)
3. Update selectors in `config.yaml`
4. Test with `test_setup.py` and a single job

**To add a resume variant:**

1. Add file path to `config.yaml` under `resumes:`
2. Reference it in platform configs with `resume_variant: <name>`
3. Can also override per-job in `open_applications_inventory.json`

**To adjust anti-bot detection:**

- Edit `config.yaml` under `anti_patterns:`
- Add keywords that indicate a blocked page

## License & Attribution

Refactored automation framework for Juan Jaramillo's job search campaign (2025).
