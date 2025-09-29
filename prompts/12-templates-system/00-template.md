# Template File

<Context>

The current integration sends user registration data from our platform's quiz to a Google Sheet, as evidenced by the #file:registros-usuarios-quizes-uk-topfinanzas-com file. The existing mechanism appends a new row for every submission, which results in duplicate entries when users register multiple times. Sometimes, we have seen as many as eight or nine registrations from the same user. Ideally, we would like to maintain one unique record per user and update their information when they submit something again.

</Context>

<Task>

Refactor the Google Sheets integration to implement an "upsert" (update or insert) logic, ensuring data integrity and preventing duplicate user records in the target spreadsheet.

### Requirements

1.  **Analyze the Current Implementation**: Review the existing code that handles the Google Sheets API connection and data submission to identify the function responsible for appending new rows.
2.  **Design an Upsert Mechanism**:
      * Before writing data, the function must perform a lookup in the target Google Sheet to determine if a record with the same unique identifier (e.g., email address) already exists.
      * If a record exists, the integration should update the corresponding row with the new data.
      * If no record exists, the integration should create a new row.
3.  **Implement the Upsert Logic**: Modify the codebase to incorporate the designed check-and-update/create functionality using the appropriate Google Sheets API methods for reading, writing, and updating data.
4.  **Validate the Solution**: Test the refactored integration to confirm that new user submissions are created correctly and that subsequent submissions from the same user update the existing record without creating a duplicate entry.

</Task>
