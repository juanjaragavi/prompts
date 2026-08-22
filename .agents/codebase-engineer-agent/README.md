# Codebase Engineer Agent

A specialized AI agent for efficient codebase analysis, debugging, and improvement across all programming languages and frameworks.

## Overview

The **Codebase Engineer Agent** is designed for developers who need deep, efficient analysis of local codebases. It prioritizes token economy and surgical precision, ensuring that every action taken is necessary and every change made is minimal yet effective.

## When to Use This Agent

Use the Codebase Engineer Agent when you need to:

- **Analyze** unfamiliar codebases or understand project architecture
- **Debug** complex issues from stack traces, error messages, or logs
- **Implement** new features that must mirror existing conventions
- **Troubleshoot** build, test, or runtime failures
- **Search** for symbols, functions, or components across the codebase
- **Enhance** UI across any frontend stack (React, Vue, Angular, etc.)
- **Investigate** git history, blame, or diff analysis
- **Modify** code with minimal, surgical changes that preserve existing style

## When NOT to Use This Agent

Avoid using this agent for:

- Full-project rewrites or large-scale refactors (unless explicitly requested)
- Modifying external systems or deploying code (unless explicitly enabled)
- Tasks requiring human visual verification (layouts, animations, visual regressions)
- Reading entire large files when targeted extraction suffices
- Resolving issues caused by missing environment variables or credentials

## Core Principles

The agent operates on five core principles:

1. **Token Economy**: Every token spent must earn its keep
2. **Evidence Over Assumption**: Never guess; always verify with targeted tool calls
3. **Scaffold First, Dive Second**: Build a structural map before examining individual files
4. **Minimal Surgical Changes**: Produce the smallest diff that correctly achieves the task
5. **Reproduce Before Fixing**: Establish failure mode with concrete evidence before fixing

## Execution Protocol

The agent follows a three-phase execution protocol:

### Phase 1: Codebase Mapping

- List repository root
- Read manifest files to extract project metadata
- Inspect configuration files
- Read concise documentation
- Build compressed mental model of the codebase

### Phase 2: Targeted Investigation

- Use grep-style tools before opening files
- Start with scoped searches, widen only if necessary
- Prefer reading specific line ranges over full files
- Use git history for context

### Phase 3: Task Execution

- **Debugging**: Collect errors → Search origin → Identify file/line → Formulate hypothesis → Apply minimal fix → Verify
- **Feature Addition**: Decompose requirements → Locate patterns → Map integration points → Implement MVP → Follow conventions → Test
- **UI Enhancement**: Locate UI layer → Inspect relevant components → Audit against goals → Make minimal changes → Verify

## Example Prompts

```bash
# Architecture analysis
"Analyze the architecture of this codebase and explain how the authentication system works"

# Debugging
"Debug why the API endpoint at `/api/users` is returning 500 errors"

# Code search
"Find all usages of the `calculateTotal` function and show me the call hierarchy"

# Feature implementation
"Implement a new feature to export data as CSV following the existing patterns in the codebase"

# Build troubleshooting
"The build is failing with error 'Module not found: xyz' - find and fix the issue"

# UI enhancement
"Enhance the user profile component to include a new avatar upload feature"

# Test debugging
"Why is the test suite failing? Identify the root cause and propose a minimal fix"

# Refactoring
"Refactor the data fetching logic in `src/utils/api.ts` to use the new caching pattern"
```

## Output Format

All responses follow structured formats:

### Debugging Reports

**Symptom** → **Root Cause** → **Fix** → **Verification**

### Feature/UI Reports

**Task** → **Approach** → **Files Touched** → **Verification**

## Quality Checks

Every response is validated against:

- **Efficiency**: Minimal necessary tool calls
- **Minimality**: Smallest correct change
- **Evidence**: Claims backed by verified results
- **Convention Adherence**: Matches existing patterns
- **Verification**: Concrete verification steps provided
- **Safety**: Secrets redacted, destructive commands confirmed
- **Clarity**: Conclusions-first, no full-file dumps
- **Scope Control**: Changes limited to relevant files

## Tool Preferences

### Preferred Tools

- `grep_search`: Fast text search across codebase
- `file_search`: Find files by glob pattern
- `read_file`: Read specific file ranges
- `list_dir`: Directory structure exploration
- `run_in_terminal`: Execute build/test commands
- `get_errors`: Check compile/lint errors
- `vscode_listCodeUsages`: Find symbol usages
- Git commands: History, blame, diff analysis

### Tools to Avoid

- Reading entire large files when targeted extraction suffices
- Stateful commands when read-only operations are sufficient
- Speculative changes without concrete evidence
- Full test suite runs when targeted tests are available

## File Structure

```
.agents/
├── codebase-engineer.agent.md    # Main agent definition
└── README.md                     # This documentation
```

## Installation

1. Place the `codebase-engineer.agent.md` file in your `.agents/` directory
2. Ensure the file has the correct `.agent.md` extension
3. Reference it in your workspace configuration if needed

## Customization

To customize this agent for your specific needs:

1. **Add domain-specific knowledge**: Include project-specific patterns or conventions
2. **Adjust tool preferences**: Modify based on your preferred workflow
3. **Extend capabilities**: Add specialized functions for your tech stack
4. **Create variants**: Fork this agent for specific use cases (e.g., frontend-only, backend-only)

## Related Agents

Consider creating these related agents for specialized tasks:

- **code-reviewer.agent.md**: Focused on code review workflows
- **debugger.agent.md**: Specialized debugging techniques
- **architect.agent.md**: System design and architectural decisions
- **refactor.agent.md**: Code refactoring and cleanup patterns

## Best Practices

1. **Start with mapping**: Always begin with codebase mapping for new projects
2. **Be specific**: Provide exact error messages, file paths, or line numbers
3. **Verify changes**: Always include verification steps in your requests
4. **Follow conventions**: The agent will mirror existing code patterns
5. **Minimal changes**: Request the smallest possible change that solves the problem

## Troubleshooting

If the agent isn't working as expected:

1. **Check file location**: Ensure `.agent.md` files are in the correct directory
2. **Verify syntax**: Agent files must be valid markdown with proper frontmatter
3. **Review scope**: Make sure your request is within the agent's capabilities
4. **Provide context**: Include relevant file paths, error messages, or code snippets

## Contributing

To improve this agent:

1. Fork the agent definition
2. Make targeted improvements
3. Test with real codebases
4. Document changes in the README
5. Share feedback on what works and what doesn't

## License

This agent definition is provided as-is for use in your development workflow. Feel free to customize it for your specific needs.
