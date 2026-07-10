# Validation Error Analysis Report

This document provides a detailed technical analysis of the validation error shown in the screenshot located at `/Users/macbookpro/Desktop/Screenshot 2026-07-10 at 4.34.49 PM.png`. It identifies the platform, specific error code, root cause, and provides a clear, step-by-step resolution plan.

---

## Description of Error

- **Platform / Service:** Google Identity / Google OAuth 2.0 Authorization Server (`accounts.google.com`)
- **Error Header:** `Access blocked: This app's request is invalid`
- **Error Code / Code Details:** `Error 400: redirect_uri_mismatch`
- **Affected User Account:** `juanamillo@gmail.com`
- **Context:** The error occurs during a Google OAuth 2.0 "Sign in with Google" flow, typically initiated by a third-party application or a custom-built integration attempting to obtain access credentials (such as Google Calendar, Gmail, or Google Custom Search integrations).

### Visual & Text Details

- **Visual Presentation:** Standard modern Google OAuth error interface rendered in Dark Mode. Features a centered, rounded-corner container (card) against a dark charcoal background. The Google "G" logo is visible at the top left.
- **Extracted Text:**
  - "You can't sign in because this app sent an invalid request. You can try again later, or contact the developer about this issue."
  - "If you are a developer of this app, see error details."
  - "Error 400: redirect_uri_mismatch"
- **Underlying Mechanism (Root Cause):**
  When an application starts a Google OAuth 2.0 workflow, it directs the user's browser to Google's sign-in page with parameters such as `client_id`, `response_type`, `scope`, and `redirect_uri`. Google's authentication server validates these parameters.

  The `redirect_uri` parameter specifies where Google should send the authorization code (or token) after the user successfully authenticates. To prevent hijacking and authorization code interception attacks, Google strictly requires that this parameter exactly match one of the pre-configured URLs in the application's credentials setup within the Google Cloud Console.

  The error `Error 400: redirect_uri_mismatch` means the `redirect_uri` passed in the login request (e.g., `http://localhost:3000/auth/callback` or a production callback endpoint) is not present in the authorized redirect URIs list for the specified OAuth 2.0 Client ID.

---

## Step-by-Step Resolution Plan

To resolve this redirect URI mismatch error, follow these technical configuration steps:

### Step 1: Identify the exact Redirect URI being requested

1. On the error page, click the **"error details"** link (or inspect the URL in the address bar).
2. Look for the `redirect_uri` parameter value inside the query string or under the details dropdown. It will look like `redirect_uri=http://localhost:XXXX/...` or similar.
3. Copy this exact URI. Pay extreme attention to trailing slashes (`/`), protocol (`http` vs. `https`), port numbers, and exact domain spelling, as Google's matching algorithm requires a character-for-character match.

### Step 2: Access the Google Cloud Console

1. Open a web browser and navigate to the [Google Cloud Console](https://console.cloud.google.com/).
2. Sign in with the Google Account that owns or administers the project associated with the application.
3. In the top-left dropdown, select the specific project that contains your application's OAuth 2.0 credentials.

### Step 3: Navigate to APIs & Services

1. Open the left navigation menu (hamburger icon) and select **APIs & Services**.
2. Click on **Credentials** from the submenu.

### Step 4: Edit the OAuth 2.0 Client ID

1. Scroll down to the **OAuth 2.0 Client IDs** section.
2. Find the client ID corresponding to the one being used by your application.
3. Click the pencil/edit icon (Edit OAuth client) on the right side of the row.

### Step 5: Configure Authorized Redirect URIs

1. In the Client ID configuration page, scroll down to the section titled **Authorized redirect URIs**.
2. Click the **+ ADD URI** button.
3. Paste the exact redirect URI identified in **Step 1** into the input field.
4. If your application uses multiple environments (e.g., development, staging, production), ensure all corresponding redirect URIs are added here as separate entries.

### Step 6: Save and Propagate

1. Click the **Save** button at the bottom of the page.
2. Allow up to 5 minutes for Google's authorization servers to update globally.
3. Restart or retry the "Sign in with Google" flow within your application to verify that the error is resolved.
