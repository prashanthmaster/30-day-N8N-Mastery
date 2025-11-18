# Mockdown Guide — OpenRouter Chat Model (Mistral route)

**Purpose**  
Watch Gmail ➝ normalize ➝ log to Google Sheets ➝ generate reply with **OpenRouter Chat Model** (Mistral route) ➝ reply in the same thread.

---

## ⚠️ Authentication & Keys (set first)

- **OpenRouter (preferred for this guide)**
  - Create **OPENROUTER_API_KEY** at openrouter.ai → *Dashboard → API Keys*.
  - In **n8n → Credentials → OpenRouter**, paste the key.
  - **Model route** (copy/paste): `mistralai/mistral-small-3.2-24b-instruct`  
    *(You can swap to another `mistralai/...` route.)*

- **Mistral (optional/direct)**  
  If you want to use the dedicated **Mistral** node instead of OpenRouter, create **MISTRAL_API_KEY** at console.mistral.ai and pick a `mistral-` model there. *(Not used in this OpenRouter-based flow.)*

- **Gmail OAuth2**
  - Enable Gmail API in Google Cloud, create OAuth client.
  - Redirect URI: `http://localhost:5678/rest/oauth2-credential/callback`
  - Use with **Gmail Trigger** and **Gmail: Reply to a message** nodes.

- **Google Sheets OAuth2**
  - Enable **Sheets** + **Drive** APIs and connect the **Google Sheets** node.
  - Share your spreadsheet with the same Google account used in n8n.

---

## Flow (Input ➝ Process ➝ Output)

**Gmail Trigger** ➝ **Set: Normalize Email** ➝ **Set: Sheet Info** ➝ **Google Sheets: Append** ➝ **AI Agent** *(LLM = OpenRouter Chat Model using Mistral route)* ➝ **Code (JS)** ➝ **Gmail: Reply to a message**

> Drag nodes onto the canvas in the sequence above. Connect left ➝ right.

---

## Node-by-Node Configuration

### 1) Gmail Trigger
- **Resource:** Message  
- **Operation:** Watch emails  
- **Recommended filters:**  
  - *Label IDs:* `INBOX`  
  - *Only Unread:* `true`  

**Outputs used later:** `id`, `threadId`, `from`, `to`, `subject`, `textPlain` (or `textHtml`).

---

### 2) Set — Normalize Email
**Keep Only Set:** `true` → **Add fields → String**

| Field       | Expression (copy/paste) |
|-------------|--------------------------|
| `ID`        | `{{$json.id || $json.ID}}` |
| `To Reply`  | `{{($json.to || '').split(',')[0]}}` |
| `Subject`   | `{{$json.subject}}` |
| `Body`      | `{{$json.textPlain || $json.textHtml || $json.body}}` |
| `ThreadId`  | `{{$json.threadId}}` |
| `FromEmail` | `{{($json.from || '').split('<').pop().replace('>','')}}` |

---

### 3) Set — Sheet Info
**Keep Only Set:** `false` → **Add fields → String**

| Field        | Value (edit to yours) |
|--------------|------------------------|
| `SheetDocId` | `1AbCdEf...YourSheetId...` |
| `SheetTab`   | `emails` |

> Share the Sheet with the Google account tied to n8n credentials.

---

### 4) Google Sheets — Append
- **Operation:** `Append`  
- **Document ID:** `={{$json.SheetDocId}}`  
- **Sheet Name:** `={{$json.SheetTab}}`  
- **Data → Use fields below**

| Column     | Expression |
|------------|------------|
| `timestamp`| `={{$now}}` |
| `from`     | `={{$json.FromEmail}}` |
| `to`       | `={{$json['To Reply']}}` |
| `subject`  | `={{$json.Subject}}` |
| `body`     | `={{$json.Body}}` |
| `threadId` | `={{$json.ThreadId}}` |

---

### 5) LLM = **OpenRouter Chat Model** (Mistral route) ➝ AI Agent
- **LLM Node:** *OpenRouter Chat Model*  
  - **Credentials:** your OpenRouter credential (**OPENROUTER_API_KEY**)  
  - **Model (route):** `mistralai/mistral-small-3.2-24b-instruct`

- **AI Agent** (uses the LLM as **Chat Model** input)  
  **System Prompt (copy/paste):**
  ```text
  You are BotCampus.ai, an AI assistant that replies to emails about learning resources and roadmaps.
  Offerings:
  - Roadmaps: AI, N8n No‑Code Automation, Python, Java, ML, NLP, Deep Learning, Web (HTML/CSS).
  - Courses: Beginner → Advanced paths with prerequisites, outcomes, time commitment.

  Objectives
  1) Understand intent from Subject + Body (roadmap, course info, enrollment/schedule, pricing/billing, support).
  2) Tone: friendly, concise, professional.
  3) Provide a clear, helpful reply and ask 1 clarifying question if crucial info is missing.

  Output format (STRICT)
  REPLY:
  <html>
    <p>...</p>
  </html>

  SUBJECT:
  <plain text subject>
  ```

  **User Message Template (copy/paste):**
  ```text
  Incoming Email
  ID: {{$json.ID}}
  To Reply: {{$json['To Reply']}}
  Subject: {{$json.Subject}}
  Body: {{$json.Body}}
  ```

---

### 6) Code (JavaScript) — Parse AI Output
Paste into the **Function** field:

```javascript
// Parse REPLY: <html>...</html> and SUBJECT: <text> from the LLM output
const raw =
  $json.output ||
  $json.text ||
  $json.data ||
  $json.choices?.[0]?.message?.content ||
  $json.choices?.[0]?.text ||
  '';

let body = String(raw).trim();

// Strip fenced blocks if present
if (body.startsWith('```')) {
  body = body.replace(/^```[\w-]*\s*/, '');
  if (body.endsWith('```')) body = body.slice(0, -3);
  body = body.trim();
}

const match = body.match(/REPLY:\s*([\s\S]*?)\n+SUBJECT:\s*([\s\S]*)$/i);
let replyHtml = '', replySubject = '';
if (match) {
  replyHtml = match[1].trim();
  replySubject = match[2].trim();
}

// Ensure HTML body
if (!/<[a-z][\w-]*[^>]*>/i.test(replyHtml)) {
  const esc = replyHtml.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  replyHtml = `<p>${esc.replace(/\r?\n/g,'<br>')}</p>`;
}

// Subject fallback
const upstream = $json.Subject || 'Regarding your request';
if (!replySubject) replySubject = `Re: ${String(upstream).trim()}`;

return [{ json: {
  replyHtml,
  replySubject,
  threadId: $json.ThreadId,
  to: $json['To Reply']
}}];
```

---

### 7) Gmail — Reply to a message
- **Resource:** Message  
- **Operation:** Reply  
- **Thread ID:** `={{$json.threadId}}`  
- **To:** `={{$json.to}}`  
- **Subject:** `={{$json.replySubject}}`  
- **Message:** `={{$json.replyHtml}}` *(HTML allowed)*  

---

## Test Checklist
1) Activate the workflow → send yourself a test email.  
2) Confirm a row is added to your sheet.  
3) Check the same Gmail thread for the AI-generated reply.

---

## Troubleshooting
- **OAuth access_denied:** verify redirect URI & scopes; re-run OAuth.  
- **Sheets not updating:** check Document ID/Sheet name & sharing.  
- **LLM error or 401:** confirm **OPENROUTER_API_KEY**; pick a valid Mistral route.  
- **Message sent as plain text:** switch Gmail node’s body to use `replyHtml`.

---

## Keys Summary
- **OPENROUTER_API_KEY** → OpenRouter Chat Model (choose `mistralai/...` route).  
- **MISTRAL_API_KEY** → only if using the dedicated **Mistral** node (not required here).
