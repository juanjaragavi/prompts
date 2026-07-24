# `linkedin_job_application_agent_prompt.md`

<execution_package>
Search, filter, and submit application packages for 10 freelance, contract, or hourly job opportunities fitting Juan Jaramillo's profile (Front-End Developer, Web Developer, Next.js, Astro, React) on LinkedIn Jobs.
<target_url>[https://www.linkedin.com/jobs/](https://www.linkedin.com/jobs/)</target_url>

Juan Miguel Jaramillo Gaviria
<juanamillo@proton.me>
+57 305 420 6139
Bogotá, Colombia
[https://www.linkedin.com/in/juan-jaramillo-ai/](https://www.google.com/search?q=https://www.linkedin.com/in/juan-jaramillo-ai/)
[https://github.com/juanjaragavi](https://github.com/juanjaragavi)
60
90
$60–$90 USD/hour
3500
Front-End Developer OR Web Developer OR Next.js OR React OR Astro
/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/juan-jaramillo-resume.md
/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/01 Juan Jaramillo Cover Letter 2026.pdf
/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/01 JUAN JARAMILLO Corporate Presentation.pdf
10

<action_sequence>

GOTO
[https://www.linkedin.com/jobs/](https://www.linkedin.com/jobs/)
None
<on_failure>HALT</on_failure>

WAIT_FOR_ELEMENT
Job search keyword input field
None
<on_failure>RELOAD</on_failure>

TYPE
Job search keyword input field
$SEARCH_KEYWORDS
<on_failure>HALT</on_failure>

CLICK
Job search submit button
None
<on_failure>HALT</on_failure>

CLICK
Filter button: 'Job Type' -> Select 'Contract', 'Part-time', or 'Temporary'
None
<on_failure>CONTINUE</on_failure>

CLICK
Filter button: 'Easy Apply'
None
<on_failure>CONTINUE</on_failure>

LOOP_START
Job listings container
Until applied_count == $TARGET_APPLICATION_COUNT or no more results
<on_failure>HALT</on_failure>

CLICK
Next unprocessed job card in search results panel
None
<on_failure>SKIP_TO_NEXT_LISTING</on_failure>

EXTRACT
Job description, employment type, rate, and title text
Verify contract/freelance/hourly nature and relevance to modern Web/Front-End/React/Next.js/Astro
<on_failure>SKIP_TO_NEXT_LISTING</on_failure>

CLICK
'Easy Apply' or 'Apply' button on job detail pane
None
<on_failure>SKIP_TO_NEXT_LISTING</on_failure>

TYPE
Phone number input field (if empty)
$PHONE
<on_failure>CONTINUE</on_failure>

TYPE
Email address input field (if empty)
$EMAIL
<on_failure>CONTINUE</on_failure>

TYPE
Desired compensation / hourly rate input field (if asked)
$HOURLY_RATE_MIN
<on_failure>CONTINUE</on_failure>

SELECT
Demographic / EEO drop-down fields (if required)
Prefer not to say
<on_failure>CONTINUE</on_failure>

TYPE
Resume file input field
$RESUME_FILE_PATH
<on_failure>CONTINUE</on_failure>

TYPE
Cover letter file input or text box (if present)
$COVER_LETTER_FILE_PATH
<on_failure>CONTINUE</on_failure>

CLICK
'Next' or 'Review' button
None
<on_failure>CONTINUE</on_failure>

PAUSE_FOR_VERIFICATION
Application submission confirmation modal
Require manual approval before final submission
<on_failure>HALT</on_failure>

LOOP_END
Increment applied_count by 1
None
<on_failure>HALT</on_failure>

</action_sequence>
<safety_checkpoint required="true">Do not click final submit offer/contract acceptance, sign contracts, consent to background checks, or provide government ID/bank details. Pause for explicit user authorization prior to executing the final 'Submit Application' click on each job modal.</safety_checkpoint>
</execution_package>
