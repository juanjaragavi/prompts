#!/bin/bash
# Job Application Bot - Helper Script

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║  Job Application Bot - Helper Script   ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
}

activate_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
        python3 -m venv "$VENV_DIR"
        source "$VENV_DIR/bin/activate"
        pip install --upgrade pip > /dev/null 2>&1
        pip install -r "$PROJECT_DIR/requirements.txt" > /dev/null 2>&1
        echo -e "${GREEN}✓ Virtual environment created and dependencies installed${NC}"
    else
        source "$VENV_DIR/bin/activate"
    fi
}

test_setup() {
    echo -e "${YELLOW}Running setup tests...${NC}"
    python3 "$PROJECT_DIR/test_setup.py"
    echo ""
}

run_applications() {
    echo -e "${YELLOW}Running job applications...${NC}"
    if [ ! -f "$PROJECT_DIR/open_applications_inventory.json" ]; then
        echo -e "${RED}✗ Inventory file not found!${NC}"
        echo "Please create 'open_applications_inventory.json' first."
        echo "Template: open_applications_inventory_template.json"
        return 1
    fi
    
    python3 "$PROJECT_DIR/apply_all_refactored.py"
}

view_logs() {
    LATEST_LOG=$(ls -t "$PROJECT_DIR/logs"/bot_*.log 2>/dev/null | head -1)
    if [ -z "$LATEST_LOG" ]; then
        echo -e "${RED}No log files found${NC}"
        return 1
    fi
    echo -e "${YELLOW}Viewing: $LATEST_LOG${NC}"
    tail -f "$LATEST_LOG"
}

view_status() {
    if [ -z "$1" ]; then
        echo "Latest statuses:"
        for f in $(ls -t "$PROJECT_DIR"/application_status_*.json 2>/dev/null | head -5); do
            INDEX=$(jq -r '.index' "$f")
            STATUS=$(jq -r '.status' "$f")
            COMPANY=$(jq -r '.company' "$f")
            echo "  $INDEX. $COMPANY - $STATUS"
        done
    else
        INDEX=$1
        STATUS_FILE="$PROJECT_DIR/application_status_$INDEX.json"
        if [ ! -f "$STATUS_FILE" ]; then
            echo -e "${RED}Status file not found for index $INDEX${NC}"
            return 1
        fi
        echo -e "${GREEN}Application #$INDEX:${NC}"
        jq . "$STATUS_FILE"
    fi
}

view_screenshots() {
    SCREENSHOTS_DIR="$PROJECT_DIR/screenshots"
    if [ ! -d "$SCREENSHOTS_DIR" ] || [ -z "$(ls "$SCREENSHOTS_DIR" 2>/dev/null)" ]; then
        echo -e "${RED}No screenshots found${NC}"
        return 1
    fi
    
    if [ -z "$1" ]; then
        echo "Opening screenshots directory..."
        open "$SCREENSHOTS_DIR" 2>/dev/null || xdg-open "$SCREENSHOTS_DIR" 2>/dev/null || echo "Directory: $SCREENSHOTS_DIR"
    else
        INDEX=$1
        SCREENSHOT=$(ls -1 "$SCREENSHOTS_DIR"/application_${INDEX}_*.png 2>/dev/null | head -1)
        if [ -z "$SCREENSHOT" ]; then
            echo -e "${RED}Screenshot not found for index $INDEX${NC}"
            return 1
        fi
        echo "Opening screenshot: $SCREENSHOT"
        open "$SCREENSHOT" 2>/dev/null || xdg-open "$SCREENSHOT" 2>/dev/null || echo "File: $SCREENSHOT"
    fi
}

stats() {
    echo -e "${YELLOW}Application Statistics:${NC}"
    
    TOTAL=$(ls -1 "$PROJECT_DIR"/application_status_*.json 2>/dev/null | wc -l)
    echo "Total applications processed: $TOTAL"
    
    if [ $TOTAL -gt 0 ]; then
        SUBMITTED=$(grep -l '"Submitted"' "$PROJECT_DIR"/application_status_*.json 2>/dev/null | wc -l)
        FILLED=$(grep -l '"Form Filled"' "$PROJECT_DIR"/application_status_*.json 2>/dev/null | wc -l)
        BLOCKED=$(grep -l '"Blocked' "$PROJECT_DIR"/application_status_*.json 2>/dev/null | wc -l)
        MANUAL=$(grep -l '"Requires Manual' "$PROJECT_DIR"/application_status_*.json 2>/dev/null | wc -l)
        
        echo "  ✓ Submitted: $SUBMITTED"
        echo "  ≈ Form Filled (no submit): $FILLED"
        echo "  ⚠ Blocked by Anti-Bot: $BLOCKED"
        echo "  ⓘ Requires Manual Action: $MANUAL"
        
        SUCCESS_RATE=$((SUBMITTED * 100 / TOTAL))
        echo ""
        echo -e "Success rate: ${GREEN}$SUCCESS_RATE%${NC}"
    fi
}

show_help() {
    cat << EOF
Usage: ./run.sh [COMMAND] [OPTIONS]

Commands:
  setup              Run tests to verify configuration
  run                Run job applications
  logs               View latest application log
  status [INDEX]     View application status (or latest if no INDEX)
  screenshots [INDEX] Open screenshots (or directory if no INDEX)
  stats              Show application statistics
  help               Show this help message

Examples:
  ./run.sh run                    # Run all jobs in inventory
  ./run.sh status 1               # View status of application #1
  ./run.sh screenshots 2          # View screenshot of application #2
  ./run.sh logs                   # Follow latest log
  ./run.sh stats                  # Show stats

First Time:
  1. Edit config.yaml (if needed)
  2. Create open_applications_inventory.json
  3. Run: ./run.sh setup
  4. Run: ./run.sh run
  5. Run: ./run.sh stats

EOF
}

# Main
print_header
activate_venv

case "${1:-help}" in
    setup)
        test_setup
        ;;
    run)
        run_applications
        ;;
    logs)
        view_logs
        ;;
    status)
        view_status "$2"
        ;;
    screenshots)
        view_screenshots "$2"
        ;;
    stats)
        stats
        ;;
    help)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac

echo ""
