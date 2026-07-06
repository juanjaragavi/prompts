# Prompt: Automated Job Application Submission

## Browser Execution Sequence

**Status:** Active Session (Stateless)

**Objective:** Parse the attached résumé, scan the current job listing tab, and apply to the first 5 job offerings, prioritizing "Easy Apply" opportunities.

---

### Phase 1: Context Ingestion & Initialization

1. **EXTRACT data** from `attached_resume.pdf`
   - _Action:_ Parse contact information, employment history, skills, and education.
   - _State:_ Map data to temporary, volatile session memory for automated form-filling.

2. **WAIT for element** `css=.jobs-search-results-list` (Timeout: 5s)
   - _Purpose:_ Verify that the job opportunities list has fully rendered on the current open tab.

3. **EXTRACT data** from visible job card elements (`css=.job-card-container`)

- _Action:_ Identify and index the first 5 available job listings. Prioritize listings displaying the "Easy Apply" badge.

---

### Phase 2: Execution Loop (Target: 5 Applications)

`Set counter: applied_count = 0`

#### **For Each Target Job Card (1 through 5):**

#### **Step 2.1: Select and Open Job**

1. **CLICK element** `css=.job-card-container[index]`
2. **WAIT for element** `css=.jobs-search__job-details` (Timeout: 5s)
3. **ASSERT** presence of application button.

#### **Step 2.2: Determine Application Path**

- **Scenario A: "Easy Apply" Button Present (Preferred)**

1. **CLICK element** `css=button.jobs-apply-button[data-job-id]` (Launches the LinkedIn application modal).
2. **WAIT for element** `css=.artdeco-modal` (Timeout: 5s).
3. **WHILE** `css=button[aria-label="Next"]` or `css=button[aria-label="Review"]` is visible:
   - **TYPE text** / **SELECT options** in form fields using the mapped résumé data.
   - **CLICK element** `css=button[aria-label*="Next"]`.

4. **CLICK element** `css=button[aria-label="Submit application"]`.
5. **WAIT for element** `css=.artdeco-toast-item--success` to confirm successful submission.
6. `Increment applied_count by 1`.

- **Scenario B: Standard "Apply" Button Present (Fallback)**

1. **CLICK element** `css=button.jobs-apply-button` (Triggers external site redirect).
2. **WAIT for tab shift / URL change**.
3. **Pause Execution Warning:** External system navigation detected.
   - _Constraint Check:_ Because external applications may require account creation or proprietary assessments, automation will attempt basic form-fill using résumé data. If blocked by complex multi-page funnels, control will temporarily yield to the user.

4. `Increment applied_count by 1` upon user confirmation or successful submission.

---

### Phase 3: Session Wrap-Up & Safeguards

1. **ASSERT** `applied_count == 5`.
2. **PURGE memory:** Instantly delete all extracted résumé data, form fields, and session tokens from memory cache.
3. **OUTPUT Execution Report:** Present a clean list of the 5 job titles and company names successfully applied to.
