# PHASE 3 - PRODUCTION-GRADE ENHANCEMENTS

## Overview

Phase 3 adds enterprise-level features to the job automation system:
- **Puppeteer** - Superior JavaScript form handling and submission
- **APScheduler** - Automated scheduled batch runs
- **Analytics Engine** - Comprehensive tracking and reporting
- **Hardened Bot** - Production-grade reliability with retry logic and state recovery
- **Multi-Candidate Support** - Manage multiple candidate profiles
- **Health Monitoring** - Real-time status and metrics

---

## Installation

### Step 1: Install Dependencies

```bash
source venv/bin/activate

# Core scheduling and form handling
pip install apscheduler

# Puppeteer for advanced JavaScript execution (optional, for Phase 3 enhancement)
pip install pyppeteer

# Verify installations
pip list | grep -E "apscheduler|pyppeteer"
```

### Step 2: Verify Installation

```bash
python3 test_phase3_bot.py
```

Expected output:
```
✓ Config loading passed
✓ Candidate registration passed
✓ Analytics recording passed
✓ Analytics export passed
✓ Health status passed
✓ Batch structure passed
```

---

## Components

### 1. Puppeteer Handler (`puppeteer_handler.py`)

Advanced form handling with:
- Dynamic field detection via JavaScript
- Intelligent data mapping
- Retry logic with exponential backoff
- State tracking (UNINITIALIZED → LOADED → FIELDS_DETECTED → FILLED → SUBMITTED)
- Comprehensive error handling

**Key Methods:**
```python
handler = PuppeteerFormHandler(logger, config)
await handler.init_browser()
await handler.load_page(url)
fields = await handler.detect_form_fields_advanced()
await handler.fill_form_intelligent(candidate_data)
success, message = await handler.submit_form()
await handler.cleanup()
```

### 2. Scheduler Manager (`scheduler_manager.py`)

Automated job scheduling with APScheduler:
- Daily scheduling (specific time)
- Interval scheduling (every N hours)
- Custom cron expressions
- Execution history tracking
- Job statistics

**Key Methods:**
```python
scheduler = ScheduledJobManager(logger, config)
scheduler.schedule_daily_applications(hour=9, minute=0, callback)
scheduler.schedule_interval_applications(hours=4, callback)
scheduler.schedule_custom_cron("0 9 * * *", callback)
await scheduler.start_scheduler()
await scheduler.stop_scheduler()
scheduler.list_scheduled_jobs()
scheduler.get_job_stats()
```

### 3. Analytics Engine (`analytics_engine.py`)

Comprehensive tracking and reporting:
- Records every application attempt
- Tracks success/failure rates
- Platform and company analysis
- Time-series data
- Dashboard-ready summaries

**Key Methods:**
```python
analytics = AnalyticsEngine(logger, config, status_dir)
analytics.record_application(index, company, job_title, platform, status, duration)
analytics.get_summary_statistics()
analytics.get_platform_analysis()
analytics.get_company_analysis()
analytics.get_timeline_analysis(days=7)
analytics.export_report(filename)
analytics.get_dashboard_summary()
```

### 4. Hardened Production Bot (`hardened_bot.py`)

Main orchestration layer combining all components:
- Retry logic (up to 3 attempts with exponential backoff)
- Concurrency control (max 3 concurrent applications)
- Multi-candidate support
- Health monitoring
- Batch processing

**Key Methods:**
```python
bot = HardenedProductionBot(config, logger)

# Multi-candidate support
bot.register_candidate("john", profile1)
bot.register_candidate("jane", profile2)

# Process single application
result = await bot.process_application(
    url="...",
    company="...",
    job_title="...",
    platform="lever",
    candidate_name="john"
)

# Process batch with concurrency control
results = await bot.process_batch(applications, candidate_name="john")

# Schedule automated runs
await bot.schedule_batch_runs(
    applications_file="open_applications_inventory.json",
    schedule="daily",
    hour=9
)
await bot.start_scheduler()

# Monitor health
status = bot.get_health_status()
summary = bot.get_status_summary()
bot.export_analytics()
```

---

## Usage Examples

### Example 1: Single Application with Retry Logic

```python
import asyncio
from hardened_bot import HardenedProductionBot
from config import Config

async def main():
    config = Config()
    bot = HardenedProductionBot(config)
    
    result = await bot.process_application(
        url="https://jobs.lever.co/provectus/397ff529-e2e9-4774-9219-5d3060cb6df2",
        company="Provectus",
        job_title="Senior Machine Learning Engineer",
        platform="lever"
    )
    
    print(f"Status: {result['status']}")
    print(f"Duration: {result['duration']:.2f}s")
    print(f"Details: {result['details']}")

asyncio.run(main())
```

### Example 2: Batch Processing with Concurrency

```python
import asyncio
import json
from hardened_bot import HardenedProductionBot
from config import Config

async def main():
    config = Config()
    bot = HardenedProductionBot(config)
    
    # Load applications
    with open("open_applications_inventory_expanded.json") as f:
        applications = json.load(f)
    
    # Process batch (max 3 concurrent)
    results = await bot.process_batch(applications[:10])
    
    # Show results
    for i, result in enumerate(results):
        print(f"{i+1}. {result['status']} ({result['duration']:.1f}s)")

asyncio.run(main())
```

### Example 3: Multi-Candidate Support

```python
import asyncio
from hardened_bot import HardenedProductionBot
from config import Config

async def main():
    config = Config()
    bot = HardenedProductionBot(config)
    
    # Register multiple candidates
    candidate1 = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone_with_cc": "+1234567890",
        # ... other fields
    }
    candidate2 = {
        "full_name": "Jane Smith",
        "email": "jane@example.com",
        "phone_with_cc": "+0987654321",
        # ... other fields
    }
    
    bot.register_candidate("john", candidate1)
    bot.register_candidate("jane", candidate2)
    
    # Apply with different candidates
    result1 = await bot.process_application(
        url="https://...",
        company="Company A",
        job_title="Role 1",
        platform="lever",
        candidate_name="john"
    )
    
    result2 = await bot.process_application(
        url="https://...",
        company="Company B",
        job_title="Role 2",
        platform="lever",
        candidate_name="jane"
    )

asyncio.run(main())
```

### Example 4: Scheduled Batch Runs

```python
import asyncio
from hardened_bot import HardenedProductionBot
from config import Config

async def main():
    config = Config()
    bot = HardenedProductionBot(config)
    
    # Schedule daily runs at 9 AM
    bot.schedule_batch_runs(
        applications_file="open_applications_inventory_expanded.json",
        schedule="daily",
        hour=9,
        minute=0
    )
    
    # Start scheduler
    await bot.start_scheduler()
    
    # Keep running (infinite)
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await bot.stop_scheduler()

asyncio.run(main())
```

### Example 5: Analytics & Monitoring

```python
import asyncio
from hardened_bot import HardenedProductionBot
from config import Config

async def main():
    config = Config()
    bot = HardenedProductionBot(config)
    
    # Get health status
    status = bot.get_health_status()
    print(f"Candidates: {status['candidates_registered']}")
    print(f"Scheduled jobs: {len(status['scheduled_jobs'])}")
    
    # Get quick summary
    summary = bot.get_status_summary()
    print(f"Total applications: {summary['total_applications_recorded']}")
    print(f"Success rate: {summary['success_rate']:.1f}%")
    
    # Export detailed report
    report_file = bot.export_analytics()
    print(f"Report exported: {report_file}")

asyncio.run(main())
```

---

## Scheduling Formats

### Daily Run
```python
bot.schedule_batch_runs(
    applications_file="inventory.json",
    schedule="daily",
    hour=9,
    minute=0
)
```
Runs every day at 09:00.

### Every 4 Hours
```python
bot.schedule_batch_runs(
    applications_file="inventory.json",
    schedule="every_4_hours"
)
```
Runs every 4 hours.

### Hourly
```python
bot.schedule_batch_runs(
    applications_file="inventory.json",
    schedule="hourly"
)
```
Runs every hour.

### Custom Cron
```python
bot.schedule_batch_runs(
    applications_file="inventory.json",
    schedule="0 9 * * 1-5"  # 9 AM, Monday-Friday
)
```
Cron format: `minute hour day month weekday`

---

## Error Handling & Retry Logic

The hardened bot implements:

1. **Exponential Backoff**: Retries with 2^n second delays
2. **Max Retries**: 3 attempts per application
3. **Timeout Handling**: 30-second page load timeout
4. **State Recovery**: Tracks form state for recovery
5. **Exception Wrapping**: All errors logged and recorded

**Retry Flow:**
```
Attempt 1 → Failed → Wait 1s
Attempt 2 → Failed → Wait 2s
Attempt 3 → Failed → Timeout (give up)
```

---

## Production Deployment

### Option 1: Systemd Service (Linux)

Create `/etc/systemd/system/job-bot.service`:
```ini
[Unit]
Description=Job Application Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/job-bot
ExecStart=/home/botuser/job-bot/venv/bin/python3 run_scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable job-bot
sudo systemctl start job-bot
sudo systemctl status job-bot
```

### Option 2: Docker

Create `Dockerfile.phase3`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "run_scheduler.py"]
```

Build and run:
```bash
docker build -f Dockerfile.phase3 -t job-bot .
docker run -d --name job-bot job-bot
docker logs -f job-bot
```

### Option 3: Screen/Tmux Session

```bash
screen -S job-bot -d -m python3 run_scheduler.py
screen -ls
screen -r job-bot
```

---

## Monitoring Dashboard

View real-time status:
```python
import json
from hardened_bot import HardenedProductionBot

bot = HardenedProductionBot()

# Quick summary
print(json.dumps(bot.get_status_summary(), indent=2))

# Full health status
print(json.dumps(bot.get_health_status(), indent=2))
```

---

## Testing

Run the comprehensive test suite:
```bash
python3 test_phase3_bot.py
```

Tests cover:
- Config loading
- Multi-candidate registration
- Analytics recording and export
- Health monitoring
- Batch application structure
- Error handling

---

## Requirements

- Python 3.8+
- apscheduler >= 3.10.0
- pyppeteer >= 0.2.1 (optional, for Puppeteer enhancement)
- Chromium browser (auto-installed by pyppeteer)

Install all:
```bash
pip install -r requirements.txt
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Scheduler not running | Check `bot.scheduler.running`, ensure `await bot.start_scheduler()` called |
| Analytics not recording | Verify `bot.analytics.record_application()` called after each attempt |
| Puppeteer browser fails | Install: `python3 -m pyppeteer install`, ensure Chromium installed |
| Memory usage high | Reduce `max_concurrent` from 3 to 2, add manual GC cleanup |
| No report generated | Check `bot.export_analytics()` return value and logs directory permissions |

---

## Next Steps

1. Register your candidate profiles
2. Load expanded inventory (25+ roles)
3. Test single application with retry logic
4. Enable scheduling for automated runs
5. Monitor analytics and health status
6. Deploy to production (systemd/Docker/tmux)
7. Set up email alerts for failures

---

## Files Created

- `puppeteer_handler.py` - Advanced form handler
- `scheduler_manager.py` - APScheduler integration
- `analytics_engine.py` - Comprehensive tracking
- `hardened_bot.py` - Main orchestration
- `test_phase3_bot.py` - Test suite
- `PHASE3_GUIDE.md` - This documentation

**Status: ✅ Phase 3 COMPLETE - Production-grade enhancements ready for deployment**
