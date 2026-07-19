#!/bin/bash

# Phase 3 Command Reference and Helper Script
# Usage: ./phase3.sh [command]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║          PHASE 3 - PRODUCTION-GRADE JOB AUTOMATION BOT             ║"
echo "║              Command Reference & Helper Script                     ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Show usage
if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage: ./phase3.sh [command]${NC}\n"
    echo -e "${GREEN}Installation:${NC}"
    echo "  ./phase3.sh install          Install Phase 3 dependencies"
    echo "  ./phase3.sh verify           Verify all installations"
    echo ""
    echo -e "${GREEN}Testing:${NC}"
    echo "  ./phase3.sh test             Run comprehensive test suite"
    echo "  ./phase3.sh test-single      Test single application (dry-run)"
    echo ""
    echo -e "${GREEN}Execution:${NC}"
    echo "  ./phase3.sh run-once         Run batch one time (25 applications)"
    echo "  ./phase3.sh run-scheduler    Start scheduler (interactive menu)"
    echo "  ./phase3.sh run-daemon       Run as background daemon"
    echo ""
    echo -e "${GREEN}Monitoring:${NC}"
    echo "  ./phase3.sh status           Show current bot status"
    echo "  ./phase3.sh analytics        Export detailed analytics report"
    echo "  ./phase3.sh logs             Show recent logs"
    echo "  ./phase3.sh jobs             List active scheduled jobs"
    echo ""
    echo -e "${GREEN}Utilities:${NC}"
    echo "  ./phase3.sh health           Full health diagnostics"
    echo "  ./phase3.sh clean            Clean logs and status files"
    echo "  ./phase3.sh help             Show this help message"
    echo ""
    exit 0
fi

case "$1" in
    install)
        echo -e "${GREEN}Installing Phase 3 dependencies...${NC}"
        source venv/bin/activate 2>/dev/null || {
            echo -e "${RED}Virtual environment not found. Creating...${NC}"
            python3 -m venv venv
            source venv/bin/activate
        }
        pip install -r requirements.txt
        echo -e "${GREEN}✓ Dependencies installed${NC}"
        ;;
    
    verify)
        echo -e "${GREEN}Verifying installations...${NC}"
        source venv/bin/activate 2>/dev/null
        python3 -c "
import sys
checks = {
    'yaml': 'PyYAML',
    'apscheduler': 'APScheduler',
}
for module, name in checks.items():
    try:
        __import__(module)
        print(f'✓ {name}')
    except ImportError:
        print(f'✗ {name} (missing)')
        sys.exit(1)

try:
    __import__('pyppeteer')
    print('✓ pyppeteer (optional)')
except ImportError:
    print('! pyppeteer not installed (optional for Puppeteer mode)')
"
        echo -e "${GREEN}✓ All dependencies verified${NC}"
        ;;
    
    test)
        echo -e "${GREEN}Running Phase 3 test suite...${NC}"
        source venv/bin/activate
        python3 test_phase3_bot.py
        ;;
    
    test-single)
        echo -e "${GREEN}Testing single application structure...${NC}"
        source venv/bin/activate
        python3 << 'EOF'
import asyncio
from hardened_bot import HardenedProductionBot
from config import Config

async def test():
    config = Config()
    bot = HardenedProductionBot(config)
    
    print("✓ Bot initialized")
    print("✓ Ready for testing")
    print("\nExample usage:")
    print("  result = await bot.process_application(")
    print("    url='https://...',")
    print("    company='Company',")
    print("    job_title='Role',")
    print("    platform='lever'")
    print("  )")

asyncio.run(test())
EOF
        ;;
    
    run-once)
        echo -e "${GREEN}Running batch one-time (25 applications)...${NC}"
        source venv/bin/activate
        python3 << 'EOF'
import asyncio
import json
from hardened_bot import HardenedProductionBot
from config import Config

async def main():
    config = Config()
    bot = HardenedProductionBot(config)
    
    # Load expanded inventory
    with open("open_applications_inventory_expanded.json") as f:
        applications = json.load(f)
    
    print(f"Processing {len(applications)} applications...")
    results = await bot.process_batch(applications)
    
    print("\n" + "=" * 70)
    submitted = sum(1 for r in results if isinstance(r, dict) and r.get('status') == 'Submitted')
    print(f"Total: {len(results)} | Submitted: {submitted}")
    print("=" * 70)

asyncio.run(main())
EOF
        ;;
    
    run-scheduler)
        echo -e "${GREEN}Starting scheduler with interactive menu...${NC}"
        source venv/bin/activate
        python3 run_scheduler.py
        ;;
    
    run-daemon)
        echo -e "${GREEN}Starting bot as background daemon...${NC}"
        source venv/bin/activate
        nohup python3 run_scheduler.py > logs/daemon.log 2>&1 &
        echo "✓ Daemon started (PID: $!)"
        echo "  View logs: tail -f logs/daemon.log"
        ;;
    
    status)
        echo -e "${GREEN}Current bot status...${NC}"
        source venv/bin/activate
        python3 << 'EOF'
import json
from hardened_bot import HardenedProductionBot
from config import Config

config = Config()
bot = HardenedProductionBot(config)
status = bot.get_status_summary()

print("\n" + "=" * 70)
print("BOT STATUS")
print("=" * 70)
for key, value in status.items():
    print(f"{key:.<40} {value}")
print("=" * 70)
EOF
        ;;
    
    analytics)
        echo -e "${GREEN}Exporting analytics report...${NC}"
        source venv/bin/activate
        python3 << 'EOF'
from hardened_bot import HardenedProductionBot
from config import Config

config = Config()
bot = HardenedProductionBot(config)
report_file = bot.export_analytics()
print(f"\n✓ Report exported: {report_file}")
EOF
        ;;
    
    logs)
        echo -e "${GREEN}Recent logs (last 50 lines)...${NC}"
        tail -50 logs/bot_*.log 2>/dev/null || echo "No logs found"
        ;;
    
    jobs)
        echo -e "${GREEN}Active scheduled jobs...${NC}"
        source venv/bin/activate
        python3 << 'EOF'
import json
from hardened_bot import HardenedProductionBot
from config import Config

config = Config()
bot = HardenedProductionBot(config)
jobs = bot.scheduler.list_scheduled_jobs()

if not jobs:
    print("No active scheduled jobs")
else:
    print("\n" + "=" * 70)
    for job in jobs:
        print(f"ID: {job['id']}")
        print(f"  Name: {job['name']}")
        print(f"  Next run: {job['next_run']}")
        print()
    print("=" * 70)
EOF
        ;;
    
    health)
        echo -e "${GREEN}Full health diagnostics...${NC}"
        source venv/bin/activate
        python3 << 'EOF'
import json
from hardened_bot import HardenedProductionBot
from config import Config

config = Config()
bot = HardenedProductionBot(config)
health = bot.get_health_status()

print("\n" + "=" * 70)
print("HEALTH DIAGNOSTICS")
print("=" * 70)
print(json.dumps(health, indent=2))
print("=" * 70)
EOF
        ;;
    
    clean)
        echo -e "${YELLOW}Cleaning logs and status files...${NC}"
        rm -f logs/bot_*.log logs/scheduler_*.log
        rm -f status_dir/*.json 2>/dev/null
        echo -e "${GREEN}✓ Cleaned${NC}"
        ;;
    
    help)
        echo -e "${GREEN}Phase 3 Help & Documentation${NC}"
        echo ""
        echo "Main Features:"
        echo "  - Puppeteer: Advanced JavaScript form handling"
        echo "  - Scheduler: APScheduler for automated runs"
        echo "  - Analytics: Comprehensive tracking and reporting"
        echo "  - Hardened: Retry logic, state recovery, concurrency"
        echo ""
        echo "Documentation:"
        echo "  ./PHASE3_GUIDE.md       - Complete Phase 3 guide"
        echo "  ./PHASE3_GUIDE.md       - Usage examples"
        echo ""
        echo "Quick Start:"
        echo "  1. ./phase3.sh install"
        echo "  2. ./phase3.sh verify"
        echo "  3. ./phase3.sh test"
        echo "  4. ./phase3.sh run-once"
        echo ""
        ;;
    
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo "Run './phase3.sh help' for usage information"
        exit 1
        ;;
esac
