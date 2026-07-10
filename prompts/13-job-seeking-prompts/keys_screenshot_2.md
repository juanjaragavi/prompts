# Google Gmail Toolkit Configuration Analysis

This document summarizes the details extracted from the Google Gmail Toolkit configuration screenshot (`Screenshot 2026-07-10 at 3.55.24 PM.png`).

## Header Details

- **Modal Title:** Configure Google Gmail Toolkit
- **Service Name:** Google Gmail

## Configuration Keys & Fields

All listed fields represent environment variables or credential inputs. Each input field includes a visibility toggle (eye icon) on the right.

1. **GOOGLE_CLIENT_ID**
   - **Required:** Yes (marked with `*`)
   - **Label:** `GOOGLE_CLIENT_ID *`
   - **Placeholder:** `Enter GOOGLE_CLIENT_ID`
   - **Action/Input Required:** Paste the OAuth 2.0 Client ID for your general Google project.

2. **GOOGLE_CLIENT_SECRET**
   - **Required:** Yes (marked with `*`)
   - **Label:** `GOOGLE_CLIENT_SECRET *`
   - **Placeholder:** `Enter GOOGLE_CLIENT_SECRET`
   - **Action/Input Required:** Paste the OAuth 2.0 Client Secret corresponding to the Client ID.

3. **GOOGLE_REFRESH_TOKEN**
   - **Required:** No (Optional)
   - **Label:** `GOOGLE_REFRESH_TOKEN`
   - **Placeholder:** `Enter GOOGLE_REFRESH_TOKEN`
   - **Action/Input Required:** Paste the Google refresh token if applicable.

4. **GMAIL_GOOGLE_CLIENT_ID**
   - **Required:** Yes (marked with `*`)
   - **Label:** `GMAIL_GOOGLE_CLIENT_ID *`
   - **Placeholder:** `Enter GMAIL_GOOGLE_CLIENT_ID`
   - **Action/Input Required:** Paste the client ID specifically configured or designated for the Gmail integration.

5. **GMAIL_GOOGLE_CLIENT_SECRET**
   - **Required:** Yes (marked with `*`)
   - **Label:** `GMAIL_GOOGLE_CLIENT_SECRET *`
   - **Placeholder:** `Enter GMAIL_GOOGLE_CLIENT_SECRET`
   - **Action/Input Required:** Paste the client secret specifically for Gmail.

6. **GMAIL_GOOGLE_REFRESH_TOKEN**
   - **Required:** Yes (marked with `*`)
   - **Label:** `GMAIL_GOOGLE_REFRESH_TOKEN *`
   - **Placeholder:** `Enter GMAIL_GOOGLE_REFRESH_TOKEN`
   - **Action/Input Required:** Paste the Google Refresh Token specifically authorized with Gmail API access scopes.

## Action Buttons

- **Cancel:** Closes the credential entry modal without saving.
- **Connect:** Submits the credential inputs to authenticate and activate the Google Gmail Toolkit.
