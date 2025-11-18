
---

# Workflow: Intelligent Email Assistant (OpenRouter Qwen)

### Goal

Automatically read incoming Gmail messages, log them into Google Sheets, generate context-aware replies using the **Qwen LLM via OpenRouter**, and send back a safe, tone-matched response.

---

## Prerequisites

1. **n8n setup**

   * Use n8n Cloud or a self-hosted instance.

2. **Gmail integration**

   * Create Gmail OAuth2 credentials in n8n.
   * Scopes needed: *read* (for trigger) and *send* (for reply).

3. **Google Sheets integration**

   * Create Google Sheets OAuth2 credentials.
   * Prepare a sheet with columns: `ID`, `To Reply`, `Subject`, `Body`.
   * Note the sheet ID: `1agSsTJ4Zgp2gO_8lH9F-epvxPaTVPxEEoswvgQJD010`.

4. **OpenRouter account**

   * Sign up at openrouter.ai, generate an API key.
   * Add this API key to n8n as OpenRouter credentials.
   * Model to use: `qwen/qwen3-235b-a22b:free`.

---

## Steps

### Step 1: Capture and Normalize Emails

* Add **Gmail Trigger** to watch for new emails.
* Pass output into a **Set node (Normalize Email)**. Map:

  * `Id` = `{{$json.id}}`
  * `To send` = `{{$json.From}}`
  * `Subject` = `{{$json.Subject}}`
  * `Body` = `{{$json.snippet}}`

This ensures clean, consistent fields.

---

### Step 2: Log Emails into Google Sheets

* Add **Set node (Sheet Id)** to store sheet ID and URL.
* Add **Google Sheets node (Append row)** to record every email into your sheet, mapping the fields:

  * `ID`, `To Reply`, `Subject`, `Body`.

---

### Step 3: Generate Reply with AI Agent

* Add **AI Agent (LangChain Agent)** node.
* Connect it to **OpenRouter Chat Model** (Qwen 3 235b free).
* Use this **prompt** in the Agent node:

```
You are BotCampus.ai, an AI assistant that replies to emails about learning resources and roadmaps.

Inputs:
- ID: {{$json.ID}}
- To Reply: {{$json['To Reply']}}
- Subject: {{$json['Subject ']}}
- Body: {{$json.Body}}

Objectives:
1. Understand intent (roadmap request, pricing, support, etc.).
2. Match tone:
   - Corporate senders → formal (no emojis).
   - Personal/free mailboxes → casual (friendly, at most 1 emoji).
3. Be accurate and safe:
   - Do not invent links, prices, or dates.
   - If risky content, output first line: {"needs_human": true, "category": "...", "confidence": 0.72}
4. Be helpful:
   - Suggest the most relevant roadmap/course.
   - Give actionable next steps.
   - Keep replies short (120–180 words).
5. Style:
   - Greet by name if possible.
   - Close with a professional, friendly sign-off.

Output format:
REPLY:
<plain text reply>

SUBJECT:
<reply subject line>
```

---

### Step 4: Parse AI Output

* Add **Code node (JavaScript)**.
* Script extracts `REPLY` and `SUBJECT`, and handles optional escalation JSON.
* Falls back to `Re: {Subject}` if no subject is provided.

---

### Step 5: Send the Reply

* Add **Gmail node (Reply to a message)**.
* Map:

  * `MessageId` = `={{$('Append row in sheet').item.json.ID}}`
  * `Message` = `={{$json.replyText}}`
  * `Subject` = `={{$json.replySubject}}`
* Sender name: “BotCampus AI Team”.

---

## Final Flow

1. Gmail Trigger → Normalize Email → Sheet Id → Append row in sheet
2. Append row in sheet → AI Agent (with OpenRouter Qwen) → Code Parser → Gmail Reply

This creates a closed-loop **Intelligent Email Assistant** that can handle inbound emails, keep a record, generate thoughtful replies, and send them automatically.

---
