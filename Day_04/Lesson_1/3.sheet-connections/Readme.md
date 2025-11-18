# README.md

# Daily Standup → Google Sheets (n8n Form to Sheet)
One-line goal: Collect a Daily Tech Standup via an **n8n Form** and append each submission as a new row in **Google Sheets**.

## At-a-glance outcomes
- Shareable **Form URL** (e.g., `https://YOUR_N8N/forms/standup`)
- Each submission → **one new row** in Google Sheets (tab **Standups**)
- Auto timestamp via `{{$now}}` (ISO)

## Prereqs & Auth (do this first)
- **Google Cloud Console**
  - Enable **Google Sheets API** for your project
- **n8n → Credentials**
  - Create **Google Sheets OAuth2 API** (or **Google API**)
  - **Redirect URI** → `https://YOUR_N8N_DOMAIN/rest/oauth2-credential/callback`
  - Connect → approve Google scopes
- **Sheet access**: the Google account used in n8n must have access to the target spreadsheet

## Architecture snapshot (nodes/tools)
- **Form Trigger** → **Google Sheets (Append Row)**
- *(Optional)* **Set** (if you want to pre-create `date_iso = {{$now}}`)

## Step-by-Step
1) **Create the Google Sheet**
   ➜ a. Create spreadsheet: **Daily Standup Log**  
   ➜ b. Rename first tab: **Standups**  
   ➜ c. Row-1 headers (exactly):  
   `employee_name | email | date_iso | project | yesterday | today | blockers | priority | tags`  
   ➜ d. Copy the **full spreadsheet URL** (we’ll paste in n8n)

2) **Build the Form (Form Trigger)**
   ➜ a. Drag **Form Trigger** to canvas → open settings  
   ➜ b. **Path**: `forms/standup`  
   ➜ c. **Form Title**: `Daily Tech Standup`  
   ➜ d. **Description**: `Quick daily report for the engineering team`  
   ➜ e. **Fields** (Name must match exactly)
      - Employee Name → **Text**, required, **Name**: `employee_name`  
      - Email → **Email**, required, **Name**: `email`  
      - Project → **Text**, required, **Name**: `project`  
      - Yesterday → **Textarea**, required, **Name**: `yesterday`  
      - Today → **Textarea**, required, **Name**: `today`  
      - Blockers → **Textarea**, optional, **Name**: `blockers`  
      - Priority → **Select**, required, **Name**: `priority`, options: `low, medium, high`  
      - Tags → **Text**, optional, **Name**: `tags` (comma-separated)

3) **Append to Google Sheets**
   ➜ a. Drag **Google Sheets** node to canvas (right of Form)  
   ➜ b. Connect **Form Trigger → Google Sheets**  
   ➜ c. **Resource**: `Sheet Within Document`  
   ➜ d. **Operation**: `Append Row`  
   ➜ e. **Document**: `By URL` → paste the spreadsheet URL  
   ➜ f. **Sheet**: `Standups`  
   ➜ g. **Mapping Mode**: `Map Each Column Manually`  
   ➜ h. **Value Input Mode**: `RAW`  
   ➜ i. **Values to Send** (copy-paste from the block below)
   employee_name = ={{ $json["employee_name"] }}
email = ={{ $json["email"] }}
date_iso = ={{ $now }}
project = ={{ $json["project"] }}
yesterday = ={{ $json["yesterday"] }}
today = ={{ $json["today"] }}
blockers = ={{ $json["blockers"] }}
priority = ={{ $json["priority"] }}
tags = ={{ $json["tags"] }}

## Copy-Paste blocks (complete)
### Google Sheets → Values to Send (each column mapping)
### (Optional) Set node between Form and Sheets
Field: date_iso
Value: ={{ $now }}
Then in Sheets map: `date_iso = ={{ $json["date_iso"] }}`

## Testing & Validation
1) **Save** the workflow  
2) **Execute workflow**  
3) In **Form Trigger**, click **Open form** → fill and **Submit**  
4) Open the spreadsheet → **Standups** tab → confirm a **new row**  
5) Validate ISO timestamp, priority value, and optional fields

## Troubleshooting
- **Auth popup fails / permission denied** → Reconnect Google credential; ensure **Sheets API** is enabled; confirm account access to spreadsheet  
- **Sheet not found / wrong tab** → Use **Document = By URL** and **Sheet = Standups** (tab name must match)  
- **Empty columns** → Form **Name** must match expression key (e.g., `employee_name`)  
- **High volume / bursts** → Insert a short **Wait** (250–500 ms) before Sheets node  
- **Form URL 404** → Check **Path** and set workflow **Active** for production

