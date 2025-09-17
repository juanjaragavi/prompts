#!/bin/sh
# example_llm_integration.sh - Example of how an LLM agent would integrate with commit_and_push.sh

# This script demonstrates how an LLM agent would:
# 1. Analyze changes in the repository
# 2. Generate an appropriate commit message
# 3. Write it to the expected file for commit_and_push.sh to consume

set -e

echo "=== Example LLM Integration for Git Commits ==="
echo ""

# Function to analyze staged changes (simulating LLM analysis)
analyze_changes() {
    echo "Analyzing repository changes..."
    echo "----------------------------------------"
    
    # Get list of changed files
    echo "Modified files:"
    git diff --cached --name-status | while read status file; do
        echo "  [$status] $file"
    done
    
    # Get statistics
    echo ""
    echo "Change statistics:"
    git diff --cached --stat
    
    echo ""
}

# Function to generate commit message (simulating LLM generation)
generate_commit_message() {
    echo "Generating commit message based on changes..."
    
    # In a real scenario, the LLM would analyze the changes and generate
    # an appropriate message. Here we're creating a simple example.
    
    # Count the number of files changed
    FILES_CHANGED=$(git diff --cached --name-only | wc -l | tr -d ' ')
    
    # Get the primary change type
    if git diff --cached --name-only | grep -q "^scripts/"; then
        PRIMARY_CHANGE="Add automation scripts"
    elif git diff --cached --name-only | grep -q "^prompts/"; then
        PRIMARY_CHANGE="Update prompts"
    elif git diff --cached --name-only | grep -q "^documents/"; then
        PRIMARY_CHANGE="Update documentation"
    else
        PRIMARY_CHANGE="Update repository files"
    fi
    
    # Build commit message
    COMMIT_MSG="$PRIMARY_CHANGE

Changes include:"
    
    # Add file-specific details
    git diff --cached --name-only | while read file; do
        if [ -n "$file" ]; then
            # Determine action based on git status
            if git status --porcelain | grep -q "^A.*$file"; then
                COMMIT_MSG="$COMMIT_MSG
- Add $file"
            elif git status --porcelain | grep -q "^M.*$file"; then
                COMMIT_MSG="$COMMIT_MSG
- Modify $file"
            elif git status --porcelain | grep -q "^D.*$file"; then
                COMMIT_MSG="$COMMIT_MSG
- Delete $file"
            fi
        fi
    done
    
    echo "$COMMIT_MSG"
}

# Main execution
main() {
    # Check if we're in a git repository
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        echo "Error: Not in a Git repository"
        exit 1
    fi
    
    # Check if there are staged changes
    if [ -z "$(git diff --cached --name-only)" ]; then
        echo "No staged changes found."
        echo "Please stage changes first with 'git add' before running the commit workflow."
        exit 1
    fi
    
    # Analyze the changes
    analyze_changes
    
    # Generate commit message
    MESSAGE=$(generate_commit_message)
    
    echo "Generated commit message:"
    echo "----------------------------------------"
    echo "$MESSAGE"
    echo "----------------------------------------"
    
    # Write to the commit message file
    COMMIT_MSG_FILE="${COMMIT_MSG_FILE:-.llm_commit_message.txt}"
    echo "$MESSAGE" > "$COMMIT_MSG_FILE"
    
    echo ""
    echo "✓ Commit message saved to: $COMMIT_MSG_FILE"
    echo ""
    echo "The commit_and_push.sh script will now detect this file and proceed with the commit."
}

# Run if executed directly
if [ "${1:-}" != "--source-only" ]; then
    main "$@"
fi