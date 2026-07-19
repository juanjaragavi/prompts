# Quick Reference - Job Application Bot

## 🚀 Quick Start

```bash
# 1. One-time setup
cd /path/to/project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 test_setup.py

# 2. Add jobs to open_applications_inventory.json
# 3. Run applications
python3 apply_all_refactored.py

# 4. Check results
ls logs/
ls application_status_*.json
ls screenshots/
```

## 📁 File Structure

```
├── config.yaml                      ← Edit this: candidate data, resume paths, platform selectors
├── config.py                        ← Config loader (no edit needed)
├── job_application_bot.py           ← Base bot class (no edit needed)
├── apply_all_refactored.py          ← Main script (ready to run)
├── test_setup.py                    ← Verify setup before running
├── requirements.txt                 ← Dependencies
├── open_applications_inventory_template.json  ← Copy this to open_applications_inventory.json
│
├── logs/                            ← Output: application logs
├── screenshots/                     ← Output: form screenshots
├── application_status_*.json        ← Output: application results
│
└── [old files - can keep for reference or archive]
    ├── apply_all_final.py          (now replaced by apply_all_refactored.py)
    ├── apply_all.py
    ├── apply_darwin.py
    └── ...20 other old scripts
```

## ⚙️ Configuration (config.yaml)

**Update these sections:**

```yaml
candidate:
  full_name: 'Your Name' # ✓ Already set
  email: 'your@email.com' # ✓ Already set
  phone: '+XX123456789' # ✓ Already set
  linkedin: 'https://linkedin.com/in/...' # ✓ Already set

resumes:
  ai_llm: '/path/to/Resume_AI_LLM.pdf' # ✓ Already set
  vibe_coding: '/path/to/Resume_Vibe.pdf' # ✓ Already set
  master: '/path/to/Resume_Master.pdf' # ✓ Already set

browser:
  headless: true # Change to false to see browser window
  timeout_ms: 40000 # Increase if pages load slowly
```

**Usually no changes needed** (unless you update resume paths):

```yaml
platforms:
  workable: # Platform selectors (pre-configured)
    selectors:
      first_name: '#firstname' # CSS selector for first name field
      email: '#email' # etc.
```

## 🎯 Job Inventory (open_applications_inventory.json)

**Template:**

```json
[
  {
    "index": 1,
    "company": "Company Name",
    "job_title": "Job Title",
    "platform": "lever",             ← Platform name (workable, lever, ashby, etc.)
    "url": "https://jobs.example.com/..."
  },
  {
    "index": 2,
    "company": "Another Company",
    "job_title": "Another Role",
    "platform": "workable",
    "url": "https://..."
  }
]
```

**Supported platforms**: `smartrecruiters`, `workable`, `lever`, `ashby`, `crelate`, `rippling`, `zoho_recruit`

## 🔍 Monitoring & Debugging

**Check logs:**

```bash
tail -f logs/bot_*.log
```

**Check application status:**

```bash
cat application_status_1.json
cat application_status_2.json
```

**View screenshots:**

```bash
open screenshots/
# or on Linux:
# ls screenshots/
```

**Common status values:**

- `Submitted` — Application successfully submitted ✓
- `Form Filled` — Form filled but submit button not found
- `Blocked by Anti-Bot` — Cloudflare/CAPTCHA detected (needs manual submission)
- `Requires Manual Action` — Form structure unknown or not supported
- `Failed to Load` — Could not access job page
- `Error` — Exception occurred

## 🛠️ Troubleshooting

| Problem                     | Solution                                                 |
| --------------------------- | -------------------------------------------------------- |
| "Config file not found"     | Ensure `config.yaml` in same directory as `config.py`    |
| "Resume file not found"     | Check absolute paths in `config.yaml`                    |
| "Selector not found"        | Check screenshots; update CSS selectors in `config.yaml` |
| "Blocked by anti-bot"       | Manual submission required; some platforms use CAPTCHA   |
| "Submit button not found"   | Form may be incomplete; check logs for missing fields    |
| "ModuleNotFoundError: yaml" | Run: `source venv/bin/activate`                          |

## 🎮 Advanced Options

**See browser in action (helpful for debugging):**

```yaml
# In config.yaml:
browser:
  headless: false
```

**Add longer delays between jobs:**
Edit `apply_all_refactored.py`, add after `bot.save_status(...)`:

```python
await asyncio.sleep(30)  # Wait 30 seconds between jobs
```

**Run only specific platform:**
Edit `apply_all_refactored.py`, modify loop:

```python
for app in inventory:
    if app['platform'].lower() != 'lever':  # Only run Lever jobs
        continue
```

**Use different resume per job:**
In `open_applications_inventory.json`:

```json
{
  "index": 1,
  "company": "Company",
  "job_title": "AI Role",
  "platform": "lever",
  "url": "...",
  "resume_variant": "ai_llm"  ← Override default
}
```

## 📊 Expected Output

```
✓ Logs:
  logs/bot_20250115_143022.log

✓ Status files (one per job):
  application_status_1.json
  application_status_2.json

✓ Screenshots:
  screenshots/application_1_20250115_143025.png
  screenshots/blocked_2_20250115_143035.png
  screenshots/error_3_20250115_143040.png
```

## 🔄 Workflow

1. **Prepare**
   - Verify `config.yaml` has correct paths
   - Run `python3 test_setup.py` to verify setup

2. **Search**
   - Find jobs on LinkedIn, job boards, etc.
   - Copy job URLs

3. **Inventory**
   - Add jobs to `open_applications_inventory.json`
   - Set correct platform (workable, lever, etc.)

4. **Run**
   - `source venv/bin/activate`
   - `python3 apply_all_refactored.py`

5. **Monitor**
   - Watch logs: `tail -f logs/bot_*.log`
   - Check screenshots for form issues
   - Review status files for results

6. **Manual Follow-up**
   - Jobs with `Blocked by Anti-Bot` status need manual submission
   - Jobs with `Requires Manual Action` may need form inspection

## 📞 Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
python3 test_setup.py

# Run applications
python3 apply_all_refactored.py

# View latest log
tail logs/bot_*.log

# Check first application status
cat application_status_1.json | jq .

# List all completed applications
for f in application_status_*.json; do
  echo "$f: $(jq -r '.status' $f)"
done

# View screenshot
open screenshots/application_1_*.png

# Count submitted applications
grep -l '"Submitted"' application_status_*.json | wc -l

# Find blocked applications
grep -l 'Blocked' application_status_*.json
```

## 🚨 If Something Goes Wrong

1. **Check the logs**

   ```bash
   tail logs/bot_*.log | grep ERROR
   ```

2. **Check the screenshot**

   ```bash
   open screenshots/error_1_*.png
   ```

3. **Check the status**

   ```bash
   cat application_status_1.json
   ```

4. **Update config if needed**
   - Wrong resume path? Update `config.yaml`
   - Selector changed? Update `platforms.<name>.selectors` in `config.yaml`

5. **Re-run just one job for testing**
   - Edit `open_applications_inventory.json` to have only 1 entry
   - Set `browser.headless: false` in `config.yaml` to see browser
   - Run `python3 apply_all_refactored.py`
   - Check screenshot to diagnose

## ✨ Pro Tips

- **Test with one job first** before running 50 at once
- **Save screenshots** for debugging form issues
- **Check logs** immediately after each run
- **Update config once, reuse everywhere** — that's the benefit of centralization!
- **Keep inventories separate** — `current_jobs.json`, `applied_this_week.json`, etc.

---

**More info**: See `REFACTORED_SETUP.md` for complete documentation
