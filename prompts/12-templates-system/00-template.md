# Template File

<Context>

An audit of the `uk.topfinanzas.com` Next.js application, conducted by founding partner and Google Ads expert Francis Lock, has identified a critical data integrity issue in our conversion tracking funnel. The number of Conversion Events fired from the Quiz page does not match the number of unique user registrations being logged in our Google Sheets database, as evidenced by the attached screenshot.

This discrepancy corrupts our marketing analytics, prevents accurate campaign performance measurement, and directly impacts monetization. The required behavior is a strict one-to-one relationship: a single user submission must trigger exactly one Conversion Event and generate one unique record in the designated Google Sheet.

</Context>

<Task>

Design and implement a robust solution to enforce a one-to-one relationship between user registrations from the Quiz, the firing of Conversion Events, and the creation of records in Google Sheets. The primary goal is to eliminate duplicate entries and ensure data accuracy.

### Requirements

1.  **Root Cause Analysis**: Investigate the end-to-end user registration flow, from the client-side submission on the Quiz page to the back-end processing. Identify the specific weaknesses in the current implementation that allow for duplicate conversion events or data entries (e.g., lack of submit button debounce, no server-side idempotent checks).
2.  **Implement a Deduplication Strategy**:
      * **Client-Side**: Harden the UI by disabling the submit button immediately upon a successful submission to prevent multiple clicks from the same user session.
      * **Server-Side**: Implement idempotent logic in the API endpoint that handles form submissions. Before processing a new registration, the server must query the Google Sheet to verify that a record for that unique user (e.g., identified by email address) does not already exist. Duplicate submissions must be rejected.
3.  **Refactor Event Firing Logic**: Modify the existing implementation to ensure the Conversion Event is fired only *after* the server has successfully validated the submission as unique and has written the new record to the Google Sheet.
4.  **Verification**: Test the solution thoroughly by simulating scenarios that would typically cause duplicates (e.g., rapid form submissions, page reloads). The implementation is considered successful when it is confirmed that for every unique user submission, exactly one Conversion Event is tracked and one corresponding row is added to the Google Sheet.

</Task>
