<prompt>

  <context>
   Source context for analysis is located in `/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts`. The implementation project for the agentic workflow must be created in the parent workspace root `/Users/macbookpro/GitHub` (outside the source prompts directory). The goal is to automate job discovery and application workflows across LinkedIn (`https://www.linkedin.com/jobs`) and third-party redirected sites for the candidate, Juan Jaramillo. The system uses an MCP (Model Context Protocol) Server and browser automation tools (including Chrome) to execute web-based job application tasks. Ollama is fully installed locally (application, service, and CLI).
  </context>

  <objective>
  Evaluate the local codebase to determine the optimal deployment architecture and implement a local, multi-agent automated job application workflow powered by local Ollama LLMs.
  </objective>

  <task>
   Conduct a diagnostic assessment of the existing codebase in `/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts` to select the target runtime architecture (Next.js application, Node.js service, or Python script via Bash), then implement the agentic workflow as a new project created under `/Users/macbookpro/GitHub` using suitable local LLMs identified via `ollama ls`.
  </task>

  <inputs>
   - Source context directory: `/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts`
   - Target project root (new implementation location): `/Users/macbookpro/GitHub`
  - Target URL: `https://www.linkedin.com/jobs` and associated external redirect URLs
  - Environment dependencies: Ollama runtime, `ollama` CLI, MCP Server, Chrome browser automation tools
  </inputs>

  <constraints>
  - Workflow execution and LLM inference must run locally.
  - Deployment runtime must be selected from three candidates: Next.js app, Node.js service, or Python script executable via Bash.
   - The final implementation codebase must be created in `/Users/macbookpro/GitHub` and must not be implemented directly inside `/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts`.
  - Browser interaction must use MCP Server integration and standard Chrome automation tooling.
  </constraints>

  <assumptions>
  - Ollama is configured and running locally with accessible models.
  - Necessary tool definitions (browser control, MCP server interfaces) are available within the execution environment.
  - Target external job boards permit standard browser automation.
  </assumptions>

  <implementation_details>
  1. Diagnostic Phase:
     - Analyze `/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts` file structure and dependencies as source context.
     - Determine the optimal runtime environment (Next.js, Node.js, or Python/Bash).
     - Define a concrete new project directory under `/Users/macbookpro/GitHub` (for example, `/Users/macbookpro/GitHub/job-application-agentic-workflow`).
  2. Model Selection:
     - Execute `ollama ls` to inspect available local models.
     - Map specific models to functional agent roles (e.g., job filtering, browser navigation, form completion).
  3. Architecture & Orchestration:
     - Implement primary agent and sub-agent communication interfaces.
     - Integrate MCP Server tooling for browser control and external site parsing.
     - Support handling redirected external job portal applications from LinkedIn links.
     - Copy and adapt any required context files, templates, examples, or configuration assets from `/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts` into the new project directory under `/Users/macbookpro/GitHub` when needed.
  </implementation_details>

  <edge_cases>
  - Unhandled external job portals requiring unsupported authentication or anti-bot verification.
  - Missing or inadequate local Ollama models for complex reasoning/parsing tasks.
  - Navigation failures or broken links during LinkedIn job redirects.
  </edge_cases>

  <acceptance_criteria>
  - Codebase diagnosis provides a clear rationale for the chosen execution framework (Next.js / Node.js / Python).
  - Selected local LLMs from `ollama ls` are successfully mapped and integrated into the workflow.
  - Agentic workflow successfully navigates LinkedIn Jobs and external redirects via MCP/Chrome integration.
  - Application tasks complete end-to-end without requiring cloud-based model endpoints.
  </acceptance_criteria>

  <validation>
  - Run `ollama ls` to verify local model availability.
  - Execute local codebase diagnostics and output framework selection.
  - Run automated test scripts against target LinkedIn Job listings and verify browser interaction and form handling logs.
  </validation>

  <deliverables>
  - Architecture evaluation report identifying the chosen framework.
   - Functional agentic workflow codebase created in a new project directory under `/Users/macbookpro/GitHub`.
   - Brief migration/context-transfer note listing which files (if any) were copied or adapted from `/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts`.
  - Execution scripts to initiate and monitor the automated application process locally.
  </deliverables>

</prompt>