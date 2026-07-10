# Google Calendar Toolkit Configuration Keys

Based on a detailed visual and OCR analysis of the configuration modal shown in the screenshot at `/Users/macbookpro/Desktop/Screenshot 2026-07-10 at 3.55.16 PM.png`, the following environment variables, configuration keys, or credential fields have been identified:

## Identified Configuration Keys & Credential Fields

### 1. `GOOGLE_CLIENT_ID`
* **Field Label:** `GOOGLE_CLIENT_ID *`
* **Status:** Required (marked with an asterisk `*`)
* **Placeholder Value:** `Enter GOOGLE_CLIENT_ID`
* **Features:** 
  * Currently focused in the UI (blue-highlighted border).
  * Includes a visibility toggle/masking icon (eye icon `👁`) on the right side of the input field.
* **Description:** The Unique Client Identifier obtained from the Google Cloud Console credentials page, used to identify the application making requests.

### 2. `GOOGLE_CLIENT_SECRET`
* **Field Label:** `GOOGLE_CLIENT_SECRET *`
* **Status:** Required (marked with an asterisk `*`)
* **Placeholder Value:** `Enter GOOGLE_CLIENT_SECRET`
* **Features:** 
  * Includes a visibility toggle/masking icon (eye icon `👁`) on the right side of the input field.
* **Description:** The secret key associated with the client ID, used to authenticate the identity of the application to the Google authorization server.

### 3. `GOOGLE_REFRESH_TOKEN`
* **Field Label:** `GOOGLE_REFRESH_TOKEN`
* **Status:** Optional / No asterisk present
* **Placeholder Value:** `Enter GOOGLE_REFRESH_TOKEN`
* **Features:** 
  * Includes a visibility toggle/masking icon (eye icon `👁`) on the right side of the input field.
* **Description:** The long-lived refresh token used to obtain new access tokens from Google OAuth without requiring manual re-authentication by the user.

---

## Modal Interface Details

* **Modal Header:** `Configure Google Calendar Toolkit` with a Close (`✕`) button.
* **Brand/Service Identifier:** Robot-head style connector icon associated with the blue `Google Calendar` text label.
* **Action Buttons:**
  * `Cancel` (Standard button to exit configuration).
  * `Connect` (Blue-filled submit button to save configuration and authorize the integration).
