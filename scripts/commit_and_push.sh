#!/bin/sh
# commit_and_push.sh - Shell script to stage, commit with LLM-provided message, and push to GitHub
# This script integrates with an LLM agent to obtain commit messages before pushing changes

set -euo pipefail  # Exit on error, undefined variables, and pipe failures

# Configuration
COMMIT_MSG_FILE="${COMMIT_MSG_FILE:-.llm_commit_message.txt}"
MAX_WAIT_SECONDS="${MAX_WAIT_SECONDS:-300}"  # 5 minutes default timeout
POLL_INTERVAL="${POLL_INTERVAL:-2}"  # Check every 2 seconds
# Commit message style: conventional | github | emoji | detailed
# - conventional: <type>(optional scope): <subject> + bullets
# - github: One-line title (<=72 chars), blank line, paragraphs/bullets, Refs
# - emoji: <emoji> <type>: <subject> + bullets
# - detailed: Sections: Summary, Changes, Rationale, Impact, Refs
COMMIT_MSG_STYLE="${COMMIT_MSG_STYLE:-conventional}"
# Optional path to write a template for the LLM to follow (will NOT be used as the commit message automatically)
COMMIT_MSG_TEMPLATE_PATH="${COMMIT_MSG_TEMPLATE_PATH:-${COMMIT_MSG_FILE}.template}"

# Colors for output (using printf for better portability)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    printf "${BLUE}[INFO]${NC} %s\n" "$1"
}

log_success() {
    printf "${GREEN}[SUCCESS]${NC} %s\n" "$1"
}

log_warning() {
    printf "${YELLOW}[WARNING]${NC} %s\n" "$1"
}

log_error() {
    printf "${RED}[ERROR]${NC} %s\n" "$1" >&2
}

# Cleanup function
cleanup() {
    if [ -f "$COMMIT_MSG_FILE" ]; then
        log_info "Cleaning up commit message file..."
        rm -f "$COMMIT_MSG_FILE"
    fi
}

# Error handler
handle_error() {
    local exit_code=$?
    log_error "Script failed with exit code: $exit_code"
    cleanup
    exit $exit_code
}

# Set up error handling
trap handle_error ERR
# Function to show style-specific commit message guidance
print_commit_message_guidance() {
    log_info "Commit message style: ${COMMIT_MSG_STYLE}"
    log_info "Save the final commit message to: ${COMMIT_MSG_FILE}"
    log_info "Optional: A template/example will be written to: ${COMMIT_MSG_TEMPLATE_PATH} (for reference)"

    # Create template directory if needed
    tpl_dir=$(dirname "${COMMIT_MSG_TEMPLATE_PATH}")
    if [ ! -d "${tpl_dir}" ]; then
        mkdir -p "${tpl_dir}" 2>/dev/null || true
    fi

    # Write a style-specific example/template for convenience
    case "${COMMIT_MSG_STYLE}" in
        conventional)
            cat > "${COMMIT_MSG_TEMPLATE_PATH}" <<'EOF'
feat(scope): concise subject in imperative mood

- Bullet 1 describing what changed
- Bullet 2 with specifics
- Bullet 3 if needed

Refs: #123, ABC-456
BREAKING CHANGE: Describe any breaking change if applicable
EOF
            ;;
        github)
            cat > "${COMMIT_MSG_TEMPLATE_PATH}" <<'EOF'
Concise, descriptive title (<= 72 chars, imperative mood)

Explain what changed and why. Include context for reviewers and users.

- Bullet point highlighting a key change
- Another relevant change

Refs: #123, ABC-456
Co-authored-by: Name <email@example.com>
EOF
            ;;
        emoji)
            cat > "${COMMIT_MSG_TEMPLATE_PATH}" <<'EOF'
✨ feat: concise subject line in imperative mood

- ✅ Detail 1 of the change
- 🛠️  Implementation or refactor notes
- 🧪 Tests or validation notes

Refs: #123
EOF
            ;;
        detailed)
            cat > "${COMMIT_MSG_TEMPLATE_PATH}" <<'EOF'
Summary
A clear one-line summary (<= 72 chars, imperative mood)

Changes
- Bullet 1
- Bullet 2

Rationale
Why this change is needed and what problem it solves.

Impact
User-facing impact, performance, or breaking changes (if any).

Refs
#123, ABC-456
EOF
            ;;
        *)
            log_warning "Unknown COMMIT_MSG_STYLE='${COMMIT_MSG_STYLE}', falling back to 'conventional'"
            COMMIT_MSG_STYLE="conventional"
            print_commit_message_guidance
            return
            ;;
    esac

    log_info "A ${COMMIT_MSG_STYLE} example has been written to: ${COMMIT_MSG_TEMPLATE_PATH}"
    log_info "Guide: Use the example as a reference, then save your final message to ${COMMIT_MSG_FILE}"
}

# Function to check Git prerequisites
check_git_prerequisites() {
    log_info "Checking Git prerequisites..."
    
    # Check if Git is installed
    if ! command -v git >/dev/null 2>&1; then
        log_error "Git is not installed"
        exit 1
    fi
    
    # Check if we're inside a Git repository
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        log_error "Not inside a Git repository"
        exit 1
    fi
    
    # Check if remote is configured
    if ! git remote get-url origin >/dev/null 2>&1; then
        log_error "No 'origin' remote configured"
        exit 1
    fi
    
    log_success "All Git prerequisites met"
}

# Function to display repository context
display_repository_context() {
    log_info "Repository Context:"
    echo "  Current Directory: $(pwd)"
    echo "  Current Branch: $(git rev-parse --abbrev-ref HEAD)"
    echo "  Remote Origin: $(git remote get-url origin)"
    
    # Check if there are any changes to commit
    if [ -z "$(git status --porcelain)" ]; then
        log_warning "No changes detected in repository"
        echo -n "Do you want to continue anyway? (y/N): "
        read -r response
        if [ "$response" != "y" ] && [ "$response" != "Y" ]; then
            log_info "Exiting as no changes to commit"
            exit 0
        fi
    else
        log_info "Changes detected:"
        git status --short
    fi
}

# Function to stage changes
stage_changes() {
    log_info "Staging all changes..."
    git add -A
    
    # Verify staging
    if [ -z "$(git diff --cached --name-only)" ]; then
        log_warning "No changes staged after 'git add -A'"
        log_info "Current status:"
        git status
        exit 1
    fi
    
    log_success "Changes staged successfully"
    log_info "Staged files:"
    git diff --cached --name-only | sed 's/^/  /'
}

# Function to wait for LLM commit message
wait_for_llm_commit_message() {
    log_info "Waiting for LLM to provide commit message..."
    log_info "Expected location: $COMMIT_MSG_FILE"
    log_info "Timeout: ${MAX_WAIT_SECONDS} seconds"
    
    # Remove any existing commit message file
    if [ -f "$COMMIT_MSG_FILE" ]; then
        log_warning "Removing existing commit message file"
        rm -f "$COMMIT_MSG_FILE"
    fi
    
    # Instructions for LLM
    echo ""
    log_info "Instructions for LLM Agent:"
    echo "  1. Review the staged changes above"
    echo "  2. Generate a commit message using style: ${COMMIT_MSG_STYLE}"
    echo "  3. Use the example/template at: ${COMMIT_MSG_TEMPLATE_PATH} (optional)"
    echo "  4. Save ONLY the final commit message to: $COMMIT_MSG_FILE"
    echo "  5. The script will automatically continue once the file is detected"
    echo ""

    # Print style-specific guidance and write a template/example file for convenience
    print_commit_message_guidance
    
    # Wait for commit message file
    local elapsed=0
    while [ $elapsed -lt $MAX_WAIT_SECONDS ]; do
        if [ -f "$COMMIT_MSG_FILE" ]; then
            # Check if file has content
            if [ -s "$COMMIT_MSG_FILE" ]; then
                log_success "Commit message file detected"
                break
            else
                log_warning "Commit message file is empty, continuing to wait..."
            fi
        fi
        
        # Show progress indicator every 10 seconds
        if [ $((elapsed % 10)) -eq 0 ] && [ $elapsed -gt 0 ]; then
            printf "."
        fi
        
        sleep $POLL_INTERVAL
        elapsed=$((elapsed + POLL_INTERVAL))
    done
    
    # Check if we timed out
    if [ $elapsed -ge $MAX_WAIT_SECONDS ]; then
        log_error "Timeout waiting for commit message after ${MAX_WAIT_SECONDS} seconds"
        exit 1
    fi
    
    # Validate commit message
    if [ ! -f "$COMMIT_MSG_FILE" ] || [ ! -s "$COMMIT_MSG_FILE" ]; then
        log_error "Commit message file is missing or empty"
        exit 1
    fi
    
    # Display the commit message
    log_success "Commit message received:"
    echo "---"
    cat "$COMMIT_MSG_FILE"
    echo "---"
}

# Function to commit changes
commit_changes() {
    log_info "Creating commit with LLM-provided message..."
    
    if git commit -F "$COMMIT_MSG_FILE"; then
        log_success "Commit created successfully"
        
        # Show commit details
        log_info "Commit details:"
        git log --oneline -1
    else
        log_error "Failed to create commit"
        exit 1
    fi
}

# Function to push changes
push_changes() {
    local current_branch=$(git rev-parse --abbrev-ref HEAD)
    log_info "Pushing to origin/$current_branch..."
    
    if git push origin HEAD; then
        log_success "Changes pushed successfully to origin/$current_branch"
    else
        log_error "Failed to push changes"
        log_info "You may need to pull changes first or resolve conflicts"
        exit 1
    fi
}

# Main execution
main() {
    echo ""
    log_info "Starting LLM-integrated commit and push workflow"
    echo "=================================================="
    
    # Step 1: Check prerequisites
    check_git_prerequisites
    
    # Step 2: Display repository context
    display_repository_context
    
    # Step 3: Stage changes
    stage_changes
    
    # Step 4: Wait for LLM commit message
    wait_for_llm_commit_message
    
    # Step 5: Commit changes
    commit_changes
    
    # Step 6: Push to remote
    push_changes
    
    # Step 7: Cleanup
    cleanup
    
    echo ""
    log_success "Workflow completed successfully!"
    log_info "Your changes have been committed and pushed to GitHub"
}

# Run main function
main "$@"