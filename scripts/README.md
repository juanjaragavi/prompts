# Scripts Directory

This directory contains automation scripts for the prompts repository.

## commit_and_push.sh

A shell script that integrates with an LLM agent to obtain commit messages before pushing changes to
GitHub.

### Features

- **Automatic Git validation**: Checks repository status, branch, and remote configuration
- **Interactive staging**: Stages all changes and displays them for review
- **LLM integration**: Waits for an LLM agent to provide a commit message via a file
- **Error handling**: Comprehensive error checking with clear logging
- **Cleanup**: Automatically removes temporary files after successful execution
- **Colored output**: Uses colors to distinguish info, warnings, errors, and success messages

### Usage

#### Basic Usage

```bash
# From the repository root
./scripts/commit_and_push.sh
```

#### With Custom Configuration

```bash
# Custom commit message file location
COMMIT_MSG_FILE="my_commit.txt" ./scripts/commit_and_push.sh

# Custom timeout (in seconds)
MAX_WAIT_SECONDS=600 ./scripts/commit_and_push.sh

# Custom polling interval (in seconds)
POLL_INTERVAL=5 ./scripts/commit_and_push.sh
```

### Workflow

1. **Validation**: Checks Git prerequisites (Git installed, inside repo, remote configured)
2. **Context Display**: Shows current directory, branch, and remote information
3. **Staging**: Stages all changes using `git add -A`
4. **LLM Wait**: Waits for LLM to create a commit message file (default: `.llm_commit_message.txt`)
5. **Commit**: Creates commit with the LLM-provided message
6. **Push**: Pushes changes to the remote repository
7. **Cleanup**: Removes temporary commit message file

### Configuration Options

| Variable           | Default                   | Description                                        |
| ------------------ | ------------------------- | -------------------------------------------------- |
| `COMMIT_MSG_FILE`  | `.llm_commit_message.txt` | Path to file where LLM should write commit message |
| `MAX_WAIT_SECONDS` | `300` (5 minutes)         | Maximum time to wait for LLM commit message        |
| `POLL_INTERVAL`    | `2`                       | Seconds between checks for commit message file     |

### LLM Integration

The script expects the LLM agent to:

1. Review the staged changes displayed by the script
2. Generate an appropriate commit message
3. Save the commit message to the configured file (default: `.llm_commit_message.txt`)
4. The script will automatically detect the file and continue

### Exit Codes

- `0`: Success - changes committed and pushed
- `1`: Failure - see error message for details

### Requirements

- POSIX-compatible shell (`sh`, `bash`, `zsh`)
- Git installed and configured
- Remote repository configured as `origin`
- Write permissions to repository

### Example Session

```bash
$ ./scripts/commit_and_push.sh

[INFO] Starting LLM-integrated commit and push workflow
==================================================
[INFO] Checking Git prerequisites...
[SUCCESS] All Git prerequisites met
[INFO] Repository Context:
  Current Directory: /Users/macbookpro/GitHub/prompts
  Current Branch: main
  Remote Origin: https://github.com/juanjaragavi/prompts.git
[INFO] Changes detected:
A  scripts/commit_and_push.sh
A  scripts/README.md
[INFO] Staging all changes...
[SUCCESS] Changes staged successfully
[INFO] Staged files:
  scripts/README.md
  scripts/commit_and_push.sh
[INFO] Waiting for LLM to provide commit message...
[INFO] Expected location: .llm_commit_message.txt
[INFO] Timeout: 300 seconds

[INFO] Instructions for LLM Agent:
  1. Review the staged changes above
  2. Generate an appropriate commit message
  3. Save the commit message to: .llm_commit_message.txt
  4. The script will automatically continue once the file is detected

[SUCCESS] Commit message received:
---
Add LLM-integrated commit and push automation script

- Create scripts directory with commit_and_push.sh
- Implement Git validation and error handling
- Add LLM integration for commit message generation
- Include comprehensive documentation and configuration options
---
[INFO] Creating commit with LLM-provided message...
[SUCCESS] Commit created successfully
[INFO] Commit details:
abc1234 Add LLM-integrated commit and push automation script
[INFO] Pushing to origin/main...
[SUCCESS] Changes pushed successfully to origin/main
[INFO] Cleaning up commit message file...

[SUCCESS] Workflow completed successfully!
[INFO] Your changes have been committed and pushed to GitHub
```

### Notes

- The script uses `git add -A` to stage all changes. Modify if you need selective staging.
- The commit message file is automatically deleted after successful execution.
- If no changes are detected, the script will ask for confirmation before proceeding.
- The script uses colored output for better visibility (may not work in all terminals).

### Troubleshooting

**Script hangs waiting for commit message:**

- Ensure the LLM agent knows to create the file at the correct location
- Check if the file path is accessible and writable
- Verify the timeout hasn't been set too low

**Permission denied:**

- Make sure the script is executable: `chmod +x scripts/commit_and_push.sh`
- Verify you have write permissions in the repository

**Push fails:**

- You may need to pull changes first: `git pull origin main`
- Check for merge conflicts that need resolution
- Verify your authentication with GitHub is working
