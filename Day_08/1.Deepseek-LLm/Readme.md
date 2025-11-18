
---

# Workflow: Intelligent Email Assistant (DeepSeek v3.1 via OpenRouter)

### Goal

Monitor Gmail for new messages, log them into a Google Sheet, generate safe, context-aware replies using **DeepSeek v3.1** through OpenRouter, and send back polished HTML email responses.

---

## Prerequisites

1. **n8n environment**

   * Use n8n Cloud or a self-hosted instance.
   * Ability to import JSON workflows.

2. **Gmail integration**

   * Create Gmail OAuth2 credentials.
   * Scopes: read (for triggers) and send (for replies).

3. **Google Sheets integration**

   * Create Google Sheets OAuth2 credentials.
   * Prepare a sheet with columns: `ID`, `To Reply`, `Subject`, `Body`.
   * Example sheet ID: `1agSsTJ4Zgp2gO_8lH9F-epvxPaTVPxEEoswvgQJD010`.

4. **OpenRouter credentials**

   * Sign up at openrouter.ai and generate an API key.
   * Add this in n8n under OpenRouter credentials.
   * Model used: `deepseek/deepseek-chat-v3.1:free`.

---

## Steps

### Step 1: Capture and Normalize Emails

* **Gmail Trigger**: Watches new emails.
* **Normalize Email (Set node)**: Extracts clean fields:

  * Id = `{{$json.id}}`
  * To send = `{{$json.From}}`
  * Subject = `{{$json.Subject}}`
  * Body = `{{$json.snippet}}`

---

### Step 2: Log Emails into Google Sheets

* **Sheet Id (Set node)**: Stores sheet ID/URL.
* **Append Row in Sheet (Google Sheets node)**: Logs normalized fields into your Google Sheet for tracking.

---

### Step 3: Generate Draft with AI Agent

* **AI Agent node**:

  * Connected to **OpenRouter Chat Model (DeepSeek v3.1)**.
  * Uses your detailed prompt to ensure:

    * Detect intent (roadmap, pricing, support).
    * Match tone (formal for corporate, casual for personal).
    * Never fabricate prices, dates, or URLs.
    * Escalate with JSON if risky.
  * Output format required:

    ```
    REPLY:
    <HTML body: minimal tags like <p>, <br>, <ul>, <li>>

    SUBJECT:
    <reply subject line>
    ```

---

### Step 4: Parse the AI Output

* **Code in JavaScript node**:

  * Extracts `REPLY` (HTML body) and `SUBJECT`.
  * Handles optional escalation JSON in first line.
  * Ensures fallback subject as `Re: {original subject}`.
  * Escapes text into safe HTML if needed.

---

### Step 5: Send the Reply

* **Reply to a Message (Gmail node)**:

  * Uses original `MessageId` from Gmail Trigger.
  * Sends the parsed `replyHtml` as the message.
  * Subject mapped from `replySubject`.
  * Sender name: “Bot Campus AI Team”.

---

## Final Flow

1. Gmail Trigger → Normalize Email → Sheet Id → Append Row in Sheet
2. Append Row in Sheet → AI Agent (DeepSeek v3.1) → Code Parser → Gmail Reply

---
