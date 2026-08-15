---
name: Commit and Push
description: Stage, commit, and push all repository changes using the LLM-integrated commit_and_push.sh workflow.
---

<prompt>

<task>
Commit and push all pending changes in `/Users/macbookpro/GitHub/prompts` using the
`scripts/commit_and_push.sh` workflow, then verify the push landed and clean up
temporary artifacts.
</task>

<execution_order>
The script wipes any pre-existing message file at startup, then blocks while polling
for it. You MUST launch the script FIRST and write the message SECOND. Writing the
message before launching guarantees it is deleted.
</execution_order>

<steps>

1. **Pre-flight.** From the repo root, confirm there is something to commit:

   ```sh
   cd /Users/macbookpro/GitHub/prompts && git status --short
   ```

   If the output is empty, STOP and report "no changes to commit." Do not run the
   script — with a clean tree it blocks on an interactive `read` prompt that cannot
   be answered.

2. **Launch the script asynchronously** (it blocks for up to 300s waiting on you):

   ```sh
   cd /Users/macbookpro/GitHub/prompts && \
     COMMIT_MSG_FILE=/Users/macbookpro/GitHub/prompts/.llm_commit_message.txt \
     sh scripts/commit_and_push.sh
   ```

   The absolute `COMMIT_MSG_FILE` is required: the script resolves a relative path
   against its invocation directory, not the repo root.

3. **Wait for the polling banner.** Read the terminal output and confirm you see
   `[INFO] Waiting for LLM to provide commit message...`. Do not proceed before this
   appears.

4. **Write the commit message** to exactly
   `/Users/macbookpro/GitHub/prompts/.llm_commit_message.txt`, derived from the staged
   file list the script printed. Use Conventional Commits (`COMMIT_MSG_STYLE=conventional`):

   ```
   <type>(<scope>): <imperative subject, ≤72 chars>

   <body paragraph explaining what changed and why>

   - <specific change>
   - <specific change>
   ```

   Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`.
   Write the message content ONLY — no code fences, no commentary, no attribution
   or co-author trailers.

5. **Confirm success.** The script auto-cleans its own message files on success. Verify:

   ```sh
   cd /Users/macbookpro/GitHub/prompts && git status --short && \
     echo "local:  $(git rev-parse HEAD)" && \
     echo "remote: $(git ls-remote --heads origin main | awk '{print $1}')"
   ```

   Pass criteria: `git status --short` is empty AND local matches remote.
   If they differ, report the mismatch — do not force-push.

6. **Clean up only untracked artifacts:**

   ```sh
   cd /Users/macbookpro/GitHub/prompts && \
     rm -f .llm_commit_message.txt .llm_commit_message.txt.template \
           prompts/13-job-seeking-prompts/.llm_commit_message.txt \
           prompts/13-job-seeking-prompts/.llm_commit_message.txt.template
   ```

</steps>

<constraints>
- NEVER delete `commit_message.txt.template` or `prompts/commit_message.txt.template`.
  Both are TRACKED files, not temporary artifacts. Deleting them requires `git restore`
  to recover.
- Never use `git push --force`, `git reset --hard`, or `--no-verify`.
- Never bypass the script by running `git commit` / `git push` directly.
- If the script exits non-zero, report the error verbatim and stop. Do not retry
  blindly or improvise a workaround.
</constraints>

</prompt>
