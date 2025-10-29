# Document

<Context>

The development environment presents several active issues requiring immediate resolution to ensure a clean codebase and proper application function.

### Technical Debt and Linting Issues (Markdown)

The `VIEW_TRANSITIONS_SUMMARY.md` file exhibits **13 markdownlint violations**, indicating non-standard markdown formatting that hinders readability and consistency:

* **MD022/blanks-around-headings**: Headings are not separated from surrounding content by blank lines.
* **MD032/blanks-around-lists**: Lists are not separated from surrounding content by blank lines.
* **MD031/blanks-around-fences**: Fenced code blocks (` ``` `) are not separated from surrounding content by blank lines.
* **MD034/no-bare-urls**: A bare URL (not enclosed in `<` and `>`) is used.

### Astro Component Deprecation

The component `<ViewTransitions />`, imported from `astro:transitions`, is **deprecated** and its usage generates a TypeScript warning (`ts(6385)`). The declaration states it has been **renamed to `ClientRouter`**.

### React Runtime Errors

The terminal output shows persistent React console warnings, primarily indicating **`Warning: Invalid hook call`**. The root cause is likely one of the following:

1.  **Mismatched React Versions**: Multiple versions of React and its renderer (React DOM) are present.
2.  **Violated Rules of Hooks**: Hooks are being called conditionally, inside loops, or in non-function components.
3.  **Duplicate React Copies**: More than one copy of React exists in the application bundle.

Additional warnings include:

* **Missing `key` Prop**: Components rendered within a list (`<ul>`) are missing the unique `key` prop.
* **Invalid DOM Property**: An attempt is made to use the HTML attribute `class` instead of the correct JSX/React prop **`className`**.

</Context>

---

<Task>

Iteratively resolve all identified issues to achieve a clean development state with zero console warnings or linting problems.

### Phase 1: Address Markdown Linting

In the file `VIEW_TRANSITIONS_SUMMARY.md`, insert necessary blank lines around all headings, lists, and fenced code blocks, and enclose all bare URLs in angle brackets (`<>`) to resolve the **MD022**, **MD032**, **MD031**, and **MD034** violations.

### Phase 2: Resolve Astro Deprecation

Refactor the component usage within the project:

* Replace all instances of the deprecated `<ViewTransitions />` component with the new component: **`<ClientRouter />`**.
* Verify the import statement is updated from `import { ViewTransitions } from "astro:transitions"` to **`import { ClientRouter } from "astro:transitions"`**.

### Phase 3: Eliminate React Runtime Warnings

Systematically debug and correct the React-related runtime warnings:

1.  **Invalid Hook Call**:
    * Inspect project dependencies to ensure a **single, consistent version of React and React DOM** is used across the application. Use `npm ls react` (or equivalent) to diagnose and fix dependency tree conflicts.
    * Review components flagged by the warning to ensure all **React Hooks adhere to the Rules of Hooks**, specifically being called only at the top level of function components or custom Hooks.
2.  **Missing `key` Prop**:
    * Add a **unique `key` prop** to every element directly rendered as a child within an array map or list structure (e.g., inside `<ul>`).
3.  **Invalid DOM Property**:
    * Change the usage of the **`class`** attribute to **`className`** in the relevant JSX elements.

Success Criterion: The Problems panel must display **zero issues**, and the terminal must show **zero React warnings** upon application execution and navigation.

</Task>
