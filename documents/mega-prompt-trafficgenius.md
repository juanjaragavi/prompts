# BROWSER AGENT INSTRUCTIONS — GCP & Service Configuration for TrafficGenius

**Target project:** `traffic-genius`
**Development port:** `3080`
**Production domain:** `trafficgenius.topnetworks.co` (provisional)
**Organization:** TopNetworks, Inc.
**Purpose:** Anti-bot security dashboard with Cloud Armor rule management, CDN analytics, and BigQuery IVT analysis

You are a browser-controlling agent. Execute the following steps **in order**. After completing all steps, compile every environment variable key-value pair into the `.env.local` template at the end and return the completed block to the coding agent. Do not skip any step. Confirm each step is complete before proceeding to the next.

---

## PHASE 1 — Google Cloud Project & API Enablement

### **Step 1.1 — Create or Select GCP Project**

1. Navigate to `https://console.cloud.google.com/`
2. In the top project picker, click "New Project" (or select the existing TopNetworks project if one is already designated for traffic security)
3. Set project name: `traffic-genius`
4. Organization: Select `topnetworks.co` if available
5. Note the auto-generated **Project ID** (e.g., `traffic-genius-123456`) — this becomes `GOOGLE_CLOUD_PROJECT`
6. Note the **Project Number** (visible in the project dashboard) — record for reference
7. Click "Create" and wait for provisioning

### **Step 1.2 — Enable Required APIs**

1. Navigate to `https://console.cloud.google.com/apis/library`
2. Enable the following APIs one by one (search each name, click "Enable"):
   - **Compute Engine API** (`compute.googleapis.com`) — Required for Cloud Armor `securityPolicies` CRUD operations
   - **BigQuery API** (`bigquery.googleapis.com`) — Required for IVT analytics queries
   - **Cloud Logging API** (`logging.googleapis.com`) — Required for reading Cloud Armor request logs
   - **Cloud Monitoring API** (`monitoring.googleapis.com`) — Required for CDN metrics (cache hit ratio, latency, bandwidth)
   - **Cloud Resource Manager API** (`cloudresourcemanager.googleapis.com`) — Required for project-level operations
   - **Identity and Access Management (IAM) API** (`iam.googleapis.com`) — Required for service account management
   - **Cloud Error Reporting API** (`clouderrorreporting.googleapis.com`) — Required for application error tracking
3. Confirm each API shows "API enabled" before proceeding
4. **Verification:** Navigate to `https://console.cloud.google.com/apis/dashboard` and confirm all 7 APIs appear in the "Enabled APIs" list

---

## PHASE 2 — Cloud Armor Security Policy Setup

> **Context:** Cloud Armor is the core service TrafficGenius manages. The dashboard will read analytics (blocked requests, bot scores, geo data) and write rules (allow/deny, rate limiting, geo-blocking, WAF) via the `securityPolicies` REST API. A security policy must exist before the UI can manage it.

### **Step 2.1 — Verify or Create a Cloud Load Balancer**

1. Navigate to `https://console.cloud.google.com/net-services/loadbalancing/list/loadBalancers`
2. Check if a Global External Application Load Balancer already exists for the TopNetworks properties (e.g., fronting `us.topfinanzas.com`, `uk.topfinanzas.com`, etc.)
3. **If a load balancer already exists:**
   - Note its name — record as `CLOUD_ARMOR_LOAD_BALANCER_NAME` (for reference only, not an env var)
   - Note the backend service(s) attached to it — these are the attachment points for Cloud Armor policies
   - Skip to Step 2.2
4. **If NO load balancer exists:** One must be created. This is a complex multi-step process:
   a. Navigate to `https://console.cloud.google.com/net-services/loadbalancing/add`
   b. Select: **Application Load Balancer (HTTP/S)** → **Global external Application Load Balancer**
   c. Configure:
   - Name: `topnetworks-global-lb`
   - Frontend: Protocol HTTPS, port 443 (requires SSL certificate — use Google-managed certificate for `*.topfinanzas.com` or the specific domains)
   - Backend: Select or create a backend service pointing to the existing Compute Engine instance group or Cloud Run service hosting TopNetworks properties
     d. Click "Create" and wait for provisioning
     e. Record the load balancer name and frontend IP address

### **Step 2.2 — Create Cloud Armor Security Policy**

1. Navigate to `https://console.cloud.google.com/net-security/securitypolicies/list`
2. Click "Create Policy"
3. Configure:
   - Policy name: `topnetworks-armor-policy` — record as `CLOUD_ARMOR_POLICY_NAME`
   - Policy type: **Backend security policy** (type: `CLOUD_ARMOR`)
   - Default rule action: **Deny** (403) — this ensures a deny-by-default posture for the "Zero-Exposure" strategy
   - Description: `TopNetworks anti-bot security policy managed by TrafficGenius UI`
4. Click "Create Policy"

### **Step 2.3 — Attach Policy to Backend Service**

1. After creating the policy, you will be on the policy details page
2. Click "Apply policy to targets" (or "Apply to backend services")
3. Select the backend service(s) from the load balancer identified in Step 2.1
4. Click "Save"

### **Step 2.4 — Add Initial Allow Rules**

> **Critical:** Since the default rule is now "Deny", you MUST add allow rules for legitimate traffic before this takes effect. Without these, all traffic will be blocked.

1. On the policy details page, click "Add Rule"
2. **Rule 1 — Allow US Traffic** (priority: 1000):
   - Match: `origin.region_code == "US"`
   - Action: Allow
   - Description: `Allow US traffic`
   - Preview mode: **Enabled** (check the preview toggle — this makes the rule non-enforcing for safety)
3. Click "Add"
4. **Rule 2 — Allow UK Traffic** (priority: 1001):
   - Match: `origin.region_code == "GB"`
   - Action: Allow
   - Description: `Allow UK traffic`
   - Preview mode: **Enabled**
5. Click "Add"
6. **Rule 3 — Allow MX Traffic** (priority: 1002):
   - Match: `origin.region_code == "MX"`
   - Action: Allow
   - Description: `Allow Mexico traffic`
   - Preview mode: **Enabled**
7. Click "Add"

> **Important:** All initial rules are in PREVIEW mode. The Human Developer must review and disable preview mode to enforce rules. TrafficGenius UI will provide the interface to manage this transition.

### **Step 2.5 — Enable Cloud CDN on Backend Service**

1. Navigate to `https://console.cloud.google.com/net-services/loadbalancing/list/loadBalancers`
2. Click on the load balancer from Step 2.1
3. Click "Edit"
4. In the backend configuration, for each backend service:
   - Check "Enable Cloud CDN"
   - Cache mode: **Use origin headers** (recommended to avoid conflicts with dynamic content)
5. Click "Update"

### **Step 2.6 — Enable Request Logging**

1. Navigate to `https://console.cloud.google.com/net-services/loadbalancing/list/loadBalancers`
2. Click on the load balancer → Edit → Backend Configuration
3. For each backend service, ensure "Logging" is **enabled** with sample rate: `1.0` (100% — needed for full Cloud Armor visibility)
4. Click "Update"

### **Step 2.7 — Record Cloud Armor Identifiers**

Record the following values:

- `CLOUD_ARMOR_POLICY_NAME` = the policy name from Step 2.2 (e.g., `topnetworks-armor-policy`)
- Note the region: `global` (since this is a global backend security policy)

---

## PHASE 3 — BigQuery Dataset for IVT Analytics

> **Context:** BigQuery stores synchronized logs from Cloud Armor and Cloud CDN for deep analysis of Invalid Traffic (IVT), ad fraud patterns, and historical trend data. The TrafficGenius UI queries these datasets for Capa 3 visualizations.

### **Step 3.1 — Create BigQuery Dataset**

1. Navigate to `https://console.cloud.google.com/bigquery`
2. In the Explorer panel, click the three dots next to your project → "Create dataset"
3. Configure:
   - Dataset ID: `traffic_security_logs` — record as `BIGQUERY_DATASET`
   - Data location: `US` (multi-region)
   - Default table expiration: **None** (or 365 days if you prefer automatic cleanup)
   - Encryption: Google-managed key
4. Click "Create Dataset"

### **Step 3.2 — Create Log Sink for Cloud Armor Logs**

> This routes Cloud Armor request logs into BigQuery for analysis.

1. Navigate to `https://console.cloud.google.com/logs/router`
2. Click "Create Sink"
3. Configure:
   - Sink name: `armor-logs-to-bigquery`
   - Description: `Routes Cloud Armor security policy logs to BigQuery for TrafficGenius analysis`
4. Sink destination:
   - Select: **BigQuery dataset**
   - Dataset: Select `traffic_security_logs` (created in Step 3.1)
   - Check "Use partitioned tables" (for query performance)
5. Inclusion filter — paste the following:\

   ```bash
   resource.type="http_load_balancer"
   jsonPayload.enforcedSecurityPolicy.name!=""
   ```

6. Click "Create Sink"
7. **Note:** After the sink is active and traffic flows through the load balancer, a table will be automatically created in BigQuery (typically named after the log source, e.g., `requests`). The table name will be recorded once data arrives.

### **Step 3.3 — Create IVT Classification Table (Optional for MVP)**

1. In BigQuery, navigate to the `traffic_security_logs` dataset
2. Click "Create Table"
3. Configure:
   - Table name: `ivt_classifications`
   - Schema — add these columns manually:

     | Field Name         | Type        | Mode     | Description                        |
     | ------------------ | ----------- | -------- | ---------------------------------- |
     | `id`               | `STRING`    | REQUIRED | UUID                               |
     | `timestamp`        | `TIMESTAMP` | REQUIRED | When the classification was made   |
     | `source_ip`        | `STRING`    | REQUIRED | Client IP                          |
     | `country_code`     | `STRING`    | NULLABLE | ISO 3166-1 alpha-2                 |
     | `traffic_source`   | `STRING`    | NULLABLE | UTM source or referrer             |
     | `ivt_type`         | `STRING`    | REQUIRED | SIVT, GIVT, or CLEAN               |
     | `confidence_score` | `FLOAT`     | NULLABLE | 0.0 - 1.0                          |
     | `rule_matched`     | `STRING`    | NULLABLE | Cloud Armor rule that flagged this |
     | `action_taken`     | `STRING`    | REQUIRED | ALLOW, DENY, THROTTLE              |

   - Partitioning: By `timestamp` (DAY)
   - Clustering: By `country_code`, `ivt_type`

4. Click "Create Table"

---

#### PHASE 4 — Service Account & IAM Permissions

> **Context:** The TrafficGenius UI runs server-side and needs a service account with specific roles to read analytics and manage Cloud Armor rules.

### **Step 4.1 — Create TrafficGenius Service Account**

1. Navigate to `https://console.cloud.google.com/iam-admin/serviceaccounts`
2. Ensure you are in the correct project (the one from Phase 1)
3. Click "Create Service Account"
4. Configure:
   - Name: `traffic-genius-sa`
   - Service account ID: `traffic-genius-sa` (auto-generated from name)
   - Description: `Service account for TrafficGenius UI — Cloud Armor management, BigQuery analytics, Cloud Logging and Monitoring access`
5. Click "Create and Continue"

### **Step 4.2 — Grant IAM Roles**

On the "Grant this service account access to project" step, add the following roles **one by one**:

| Role                                                     | Purpose                                              |
| -------------------------------------------------------- | ---------------------------------------------------- |
| `Compute Security Admin` (`roles/compute.securityAdmin`) | Full CRUD on Cloud Armor security policies and rules |
| `BigQuery Data Viewer` (`roles/bigquery.dataViewer`)     | Read BigQuery datasets and tables                    |
| `BigQuery Job User` (`roles/bigquery.jobUser`)           | Execute BigQuery queries                             |
| `Logs Viewer` (`roles/logging.viewer`)                   | Read Cloud Logging entries (Armor logs)              |
| `Monitoring Viewer` (`roles/monitoring.viewer`)          | Read Cloud Monitoring metrics (CDN metrics)          |
| `Error Reporting Writer` (`roles/errorreporting.writer`) | Report application errors to GCP                     |

1. For each role: click "Add another role" → search for the role name → select it
2. After all 6 roles are added, click "Continue"
3. On the "Grant users access to this service account" step, skip (click "Done")

### **Step 4.3 — Generate Service Account Key File**

1. Click on the newly created `traffic-genius-sa` service account
2. Navigate to the "Keys" tab
3. Click "Add Key" → "Create new key" → Format: **JSON**
4. Click "Create" — the JSON key file will download automatically
5. Open the downloaded JSON file and extract:
   - `GOOGLE_CLOUD_PROJECT` = value of the `project_id` field
   - `GCP_CLIENT_EMAIL` = value of the `client_email` field
   - `GCP_PRIVATE_KEY` = value of the `private_key` field (the full multi-line PEM string — when pasting into `.env.local`, keep `\n` characters as literal `\n` escapes, not actual newlines)
6. **Save the entire JSON file** — it will be placed at `credentials/gcs-service-account.json` inside the project directory (the coding agent will handle this)
7. Record:
   - `GOOGLE_APPLICATION_CREDENTIALS` = `credentials/gcs-service-account.json`

---

#### PHASE 5 — OAuth Consent Screen & Google OAuth Credentials (Authentication)

> **Context:** TrafficGenius is an internal tool restricted to `@topnetworks.co` and `@topfinanzas.com` email domains. It uses Better Auth with Google OAuth for SSO.

### **Step 5.1 — Configure OAuth Consent Screen**

1. Navigate to `https://console.cloud.google.com/apis/credentials/consent`
2. Check if an OAuth consent screen already exists for this project
3. **If it needs to be created:**
   - Select "Internal" user type → Click "Create"
     - _(If "Internal" is not available because the project is not under a Google Workspace organization, select "External" instead)_
   - Fill in:
     - App name: `TrafficGenius`
     - User support email: `info@topnetworks.co`
     - App logo: _(skip for now)_
     - App domain — Application home page: `https://trafficgenius.topnetworks.co`
     - Developer contact email: `info@topnetworks.co`
   - Scopes: Add `email`, `profile`, `openid`
   - Test users (only if External): Add `info@topnetworks.co`, `juan.jaramillo@topnetworks.co`
   - Click "Save and Continue" through all steps

### **Step 5.2 — Create OAuth 2.0 Client ID**

1. Navigate to `https://console.cloud.google.com/apis/credentials`
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: **Web application**
4. Name: `TrafficGenius Web Client`
5. Authorized JavaScript origins — add:
   - `http://localhost:3080`
   - `https://trafficgenius.topnetworks.co`
6. Authorized redirect URIs — add:
   - `http://localhost:3080/api/auth/callback/google`
   - `https://trafficgenius.topnetworks.co/api/auth/callback/google`
7. Click "Create"
8. Copy and record:
   - `GOOGLE_CLIENT_ID` = Client ID shown
   - `GOOGLE_CLIENT_SECRET` = Client Secret shown

---

#### PHASE 6 — Supabase (PostgreSQL Database)

> **Context:** Supabase stores Better Auth session tables, Cloud Armor rule change audit logs, and user dashboard preferences. It follows the RouteGenius database pattern.

### **Step 6.1 — Create Supabase Project**

1. Navigate to `https://supabase.com/dashboard`
2. Click "New Project"
3. Organization: Select TopNetworks (or create if absent)
4. Configure:
   - Project name: `traffic-genius`
   - Database password: Generate a strong password (at least 16 characters) — **record this password securely**
   - Region: `us-west-2` (Oregon) — matches existing TopNetworks projects
   - Plan: Free tier (upgrade to Pro later for production)
5. Click "Create new project" and wait for provisioning (~2 minutes)

### **Step 6.2 — Collect Supabase Credentials**

1. Once the project is ready, navigate to: **Project Settings → API**
2. Record:
   - `NEXT_PUBLIC_SUPABASE_URL` = Project URL (format: `https://abcdefgh.supabase.co`)
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` = `anon` / `public` key
   - `SUPABASE_SERVICE_ROLE_KEY` = `service_role` key (this is secret — never expose client-side)
3. Navigate to: **Project Settings → Database**
4. Under "Connection string" → select "URI" tab → Mode: `Session` → Port: `6543`
5. Copy the connection string and replace `[YOUR-PASSWORD]` with the password from Step 6.1
6. Record:
   - `DATABASE_URL` = the full connection string (e.g., `postgresql://postgres.abcdefgh:PASSWORD@aws-0-us-west-2.pooler.supabase.com:6543/postgres`)

### **Step 6.3 — Run Better Auth Migration Tables**

1. In Supabase dashboard, navigate to: **SQL Editor**
2. Click "New Query"
3. Paste and execute the following SQL to create the Better Auth required tables:

   ```sql
   -- Better Auth schema migration for TrafficGenius
   -- Reference: https://www.better-auth.com/docs/concepts/database#schema

   CREATE TABLE IF NOT EXISTS "user" (
       id TEXT PRIMARY KEY,
       name TEXT NOT NULL,
       email TEXT NOT NULL UNIQUE,
       "emailVerified" BOOLEAN NOT NULL DEFAULT FALSE,
       image TEXT,
       "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
       "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
   );

   CREATE TABLE IF NOT EXISTS "session" (
       id TEXT PRIMARY KEY,
       "expiresAt" TIMESTAMP NOT NULL,
       token TEXT NOT NULL UNIQUE,
       "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
       "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW(),
       "ipAddress" TEXT,
       "userAgent" TEXT,
       "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE
   );

   CREATE TABLE IF NOT EXISTS "account" (
       id TEXT PRIMARY KEY,
       "accountId" TEXT NOT NULL,
       "providerId" TEXT NOT NULL,
       "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
       "accessToken" TEXT,
       "refreshToken" TEXT,
       "idToken" TEXT,
       "accessTokenExpiresAt" TIMESTAMP,
       "refreshTokenExpiresAt" TIMESTAMP,
       scope TEXT,
       password TEXT,
       "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
       "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
   );

   CREATE TABLE IF NOT EXISTS "verification" (
       id TEXT PRIMARY KEY,
       identifier TEXT NOT NULL,
       value TEXT NOT NULL,
       "expiresAt" TIMESTAMP NOT NULL,
       "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
       "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
   );
   ```

4. Click "Run" and verify all 4 tables (`user`, `session`, `account`, `verification`) are created
5. Navigate to **Table Editor** to confirm the tables appear

### **Step 6.4 — Run TrafficGenius Application Tables**

1. In SQL Editor, create a new query
2. Paste and execute:

   ```sql
   -- TrafficGenius application tables

   -- Audit log for Cloud Armor rule changes
   CREATE TABLE IF NOT EXISTS "audit_logs" (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE SET NULL,
       action TEXT NOT NULL,                    -- CREATE_RULE, UPDATE_RULE, DELETE_RULE, TOGGLE_PREVIEW
       policy_name TEXT NOT NULL,
       rule_priority INTEGER,
       before_snapshot JSONB,                   -- Rule state before change (null for CREATE)
       after_snapshot JSONB,                    -- Rule state after change (null for DELETE)
       description TEXT,                        -- Human-readable change description
       created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
   );

   CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
   CREATE INDEX idx_audit_logs_policy_name ON audit_logs(policy_name);
   CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);

   -- User dashboard preferences
   CREATE TABLE IF NOT EXISTS "dashboard_preferences" (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       user_id TEXT NOT NULL UNIQUE REFERENCES "user"(id) ON DELETE CASCADE,
       layout JSONB DEFAULT '{}',               -- Widget arrangement, collapsed panels
       refresh_interval INTEGER DEFAULT 60,     -- Auto-refresh interval in seconds
       default_date_range TEXT DEFAULT '24h',   -- Default time range for charts
       default_policy TEXT,                     -- Default Cloud Armor policy to show
       theme TEXT DEFAULT 'light',              -- UI theme preference
       created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
       updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
   );

   -- Enable Row Level Security
   ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
   ALTER TABLE dashboard_preferences ENABLE ROW LEVEL SECURITY;

   -- RLS Policies: Users can read all audit logs (transparency) but only modify own preferences
   CREATE POLICY "Users can read all audit logs"
       ON audit_logs FOR SELECT
       USING (true);

   CREATE POLICY "Users can insert own audit logs"
       ON audit_logs FOR INSERT
       WITH CHECK (true);

   CREATE POLICY "Users can read own preferences"
       ON dashboard_preferences FOR SELECT
       USING (user_id = current_setting('request.jwt.claims')::json->>'sub');

   CREATE POLICY "Users can insert own preferences"
       ON dashboard_preferences FOR INSERT
       WITH CHECK (user_id = current_setting('request.jwt.claims')::json->>'sub');

   CREATE POLICY "Users can update own preferences"
       ON dashboard_preferences FOR UPDATE
       USING (user_id = current_setting('request.jwt.claims')::json->>'sub');
   ```

3. Click "Run" and verify `audit_logs` and `dashboard_preferences` tables are created
4. Navigate to **Table Editor** to confirm

---

#### PHASE 7 — Google Analytics 4 (Optional but Recommended)

### **Step 7.1 — Create or Select GA4 Property**

1. Navigate to `https://analytics.google.com/`
2. Either:
   - Create a new GA4 property for `trafficgenius.topnetworks.co`, OR
   - Reuse an existing TopNetworks GA4 property with a new data stream
3. Go to: **Admin → Data Streams → Add stream → Web**
4. Configure:
   - Website URL: `trafficgenius.topnetworks.co`
   - Stream name: `TrafficGenius Web`
5. Record:
   - `NEXT_PUBLIC_GA_MEASUREMENT_ID` = Measurement ID (format: `G-XXXXXXXXXX`)

#### _(If GA4 is not needed for the internal tool, skip this phase and leave the env var empty — the app conditionally loads GA4 only when the ID is present.)_

---

#### PHASE 8 — Generate Better Auth Secret

### **Step 8.1 — Generate a Cryptographic Secret**

1. Open any terminal or browser-based tool that can generate random bytes
2. Generate a 32-byte random base64 string. Options:
   - In a terminal: `openssl rand -base64 32`
   - Or use an online generator: navigate to `https://generate-secret.vercel.app/32`
3. Record:
   - `BETTER_AUTH_SECRET` = the generated secret string

---

#### PHASE 9 — Final Environment Variable Compilation

Compile ALL recorded values from Phases 1–8 into the following `.env.local` template. Replace each placeholder with the actual recorded value. Return the completed block to the coding agent.

```env
# ============================================================
# APP — TrafficGenius
# ============================================================
NEXT_PUBLIC_APP_URL=http://localhost:3080
NODE_ENV=development
NEXT_PUBLIC_ENABLE_LOGGING=true

# ============================================================
# GOOGLE CLOUD PLATFORM
# ============================================================
GOOGLE_CLOUD_PROJECT=                        # Phase 1, Step 1.1: GCP Project ID
GOOGLE_APPLICATION_CREDENTIALS=credentials/gcs-service-account.json

# ============================================================
# CLOUD ARMOR
# ============================================================
CLOUD_ARMOR_POLICY_NAME=                     # Phase 2, Step 2.2: e.g., topnetworks-armor-policy

# ============================================================
# BIGQUERY
# ============================================================
BIGQUERY_DATASET=                            # Phase 3, Step 3.1: e.g., traffic_security_logs

# ============================================================
# GCP SERVICE ACCOUNT (from JSON key file)
# ============================================================
GCP_CLIENT_EMAIL=                            # Phase 4, Step 4.3: client_email from JSON
GCP_PRIVATE_KEY=                             # Phase 4, Step 4.3: private_key from JSON (keep \n as literal)

# ============================================================
# SUPABASE (PostgreSQL)
# ============================================================
NEXT_PUBLIC_SUPABASE_URL=                    # Phase 6, Step 6.2: e.g., https://abcdefgh.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=               # Phase 6, Step 6.2: anon key
SUPABASE_SERVICE_ROLE_KEY=                   # Phase 6, Step 6.2: service_role key
DATABASE_URL=                                # Phase 6, Step 6.2: full connection string with password

# ============================================================
# BETTER AUTH
# ============================================================
BETTER_AUTH_SECRET=                           # Phase 8, Step 8.1: openssl rand -base64 32
BETTER_AUTH_URL=http://localhost:3080

# ============================================================
# GOOGLE OAUTH (Authentication)
# ============================================================
GOOGLE_CLIENT_ID=                            # Phase 5, Step 5.2: OAuth Client ID
GOOGLE_CLIENT_SECRET=                        # Phase 5, Step 5.2: OAuth Client Secret

# ============================================================
# GOOGLE ANALYTICS 4 (Optional)
# ============================================================
NEXT_PUBLIC_GA_MEASUREMENT_ID=               # Phase 7, Step 7.1: G-XXXXXXXXXX (leave empty to skip)

# ============================================================
# FEATURE FLAGS (Development)
# ============================================================
DISABLE_RATE_LIMITING=true
```

---

#### CRITICAL NOTES FOR THE BROWSER AGENT

1. **Cloud Armor default-deny is in PREVIEW mode** — All initial rules were added with preview enabled. This means NO traffic will actually be blocked until the Human Developer reviews and disables preview mode. This is a safety measure.

2. **BigQuery log sink takes time** — The `armor-logs-to-bigquery` sink created in Phase 3 will only populate once real traffic flows through the load balancer. The coding agent will build the UI to handle empty datasets gracefully.

3. **Service account key security** — The JSON key file downloaded in Phase 4 contains critical credentials. It must be:
   - Saved to `credentials/gcs-service-account.json` in the project directory
   - Added to `.gitignore` (the coding agent handles this)
   - Never committed to version control

4. **`GCP_PRIVATE_KEY` formatting** — When pasting the private key into `.env.local`, the multi-line PEM key must have literal `\n` characters (not actual newlines). Example:

   ```bash
   GCP_PRIVATE_KEY="<SERVICE_ACCOUNT_PRIVATE_KEY_WITH_LITERAL_NEWLINES>"
   ```

5. **Supabase RLS** — The SQL in Phase 6.4 configures Row Level Security. The `service_role` key bypasses RLS, which is how the server-side Next.js code accesses data. The `anon` key respects RLS for any future client-side operations.

6. **Return the completed `.env.local` block** — Once all phases are complete, compile the final values and return them to the coding agent. No code will be written until these values are received.

---

## **END OF BROWSER AGENT INSTRUCTIONS**

---
