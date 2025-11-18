
---

# 𝗣𝗿𝗲𝗿𝗲𝗾𝘂𝗶𝘀𝗶𝘁𝗲𝘀

* 𝗻𝟴𝗻: access to import/create workflows.
* 𝗚𝗺𝗮𝗶𝗹 OAuth credentials: for trigger + reply.
* 𝗚𝗼𝗼𝗴𝗹𝗲 𝗦𝗵𝗲𝗲𝘁𝘀 OAuth: to log inbound emails.
* 𝗚𝗲𝗺𝗶𝗻𝗶 API key: create a **Google PaLM/Gemini** credential (your file uses **“Gemini 2.5-flash”**).

---

# 𝗪𝗼𝗿𝗸𝗳𝗹𝗼𝘄 𝗺𝗮𝗽 (from your JSON)

**Gmail Trigger → Normalize Email → Sheet Id → Append row in sheet → AI Agent**
and **Google Gemini Chat Model →(ai\_languageModel)→ AI Agent → Code in JavaScript → Reply to a message**.

---

## 1) 𝗚𝗠𝗔𝗜𝗟 𝗧𝗥𝗜𝗚𝗚𝗘𝗥 (watch new emails)

* Add **Gmail Trigger**.
* Choose the mailbox and event “New Email”.
* Enable simplified data if you prefer cleaner fields (subject/from/text).
* Output will carry the incoming **Subject/Body/Sender** used downstream. (Wired as first node in your JSON).

## 2) 𝗡𝗢𝗥𝗠𝗔𝗟𝗜𝗭𝗘 𝗘𝗠𝗔𝗜𝗟 (Set node)

Create a **Set** node named **Normalize Email** that produces the **exact keys** your prompt expects:

* **ID** → `{{$json.id || $json.messageId || $json.threadId}}`
* **To Reply** → `{{$json.from || $json.headers?.from}}`
* \*\*Subject \*\* (note the trailing space, keep it) → `{{$json.subject || $json.headers?.subject}}`
* **Subject** (no space, duplicate value for safety)
* **Body** → `{{$json.text || $json.plainText || $json.body}}`
  This feeds the Agent prompt which directly references **ID**, **To Reply**, \*\*Subject \*\*, and **Body**.

## 3) 𝗦𝗛𝗘𝗘𝗧 𝗜𝗗 (Set node)

Add a **Set** node named **Sheet Id** to store your Spreadsheet ID & Sheet name, e.g.:

* **sheetId** = `your_google_sheet_id`
* **sheetName** = `InboxLog`
  (It’s present as a distinct node before appending.)

## 4) 𝗔𝗣𝗣𝗘𝗡𝗗 𝗥𝗢𝗪 𝗜𝗡 𝗦𝗛𝗘𝗘𝗧 (Google Sheets)

Add **Google Sheets → Append**:

* Spreadsheet: `={{$json.sheetId}}`
* Sheet: `={{$json.sheetName}}`
* Columns to append: timestamp, from, subject, snippet, threadId
  This logs every inbound email prior to AI processing. (Matches your wiring.)

## 5) 𝗚𝗢𝗢𝗚𝗟𝗘 𝗚𝗘𝗠𝗜𝗡𝗜 𝗖𝗛𝗔𝗧 𝗠𝗢𝗗𝗘𝗟

Add **Google Gemini Chat Model**:

* Model: **Gemini 2.5-flash** (use your credential).
* No system prompt here; this node only supplies the LLM to the Agent.

## 6) 𝗔𝗜 𝗔𝗚𝗘𝗡𝗧 (LangChain Agent)

Add **AI Agent** node and connect it after **Append row in sheet**.

* In **Prompt Type**, choose **Define** (custom text).
* Paste the **prompt** below (it’s the cleaned version of what your JSON already carries, keeping the same structure and rules):

```
You are 𝗕𝗼𝘁𝗖𝗮𝗺𝗽𝘂𝘀.𝗮𝗶, an assistant replying to emails about learning resources and roadmaps.

Offerings you can reference at a high level:
- Roadmaps: AI, N8n No-Code Automation, Python, Java, Machine Learning, NLP, Deep Learning, Web (HTML/CSS).
- Courses: Beginner → Advanced paths across those domains.

𝗜𝗡𝗣𝗨𝗧𝗦 (from current item/json):
- ID: {{ $json.ID }}
- TO reply: {{ $json['To Reply'] }}
- Subject: {{ $json['Subject '] }}
- Body: {{ $json.Body }}

𝗢𝗕𝗝𝗘𝗖𝗧𝗜𝗩𝗘𝗦
1) Understand intent from Subject + Body (roadmap request, course info, enrollment/schedule, pricing/billing, troubleshooting/support, or other).
2) Match tone:
   - Work/corporate senders → formal (clear, concise, no emojis).
   - Personal/free mailboxes → casual (friendly, warm; at most 1 tasteful emoji).
3) Be accurate & safe:
   - Do NOT invent links, dates, or prices. If missing, ask ONE focused clarifying question or state next steps.
   - If risky (passwords, banking/wire, legal threats, harassment, phishing), set `needs_human: true`.
4) Be helpful:
   - Offer the most relevant roadmap/course path based on hints in the Body.
   - Give actionable next steps (e.g., confirm experience level, pick a start date, share goal timeline).
   - Keep replies short (~120–180 words), scannable; use a few bullets only if necessary.

𝗦𝗧𝗬𝗟𝗘
- Greet using sender’s name if present; otherwise keep neutral.
- Simple sentences; minimal jargon unless user is advanced.
- Match language if the Body is in a non-English language; else reply in English.
- Close with a friendly, professional sign-off aligned to the tone.

𝗥𝗘𝗦𝗢𝗨𝗥𝗖𝗘 𝗥𝗘𝗙𝗦
- Refer by track name (e.g., “AI Roadmap”, “N8n No-Code Automation Roadmap”).
- If URLs needed, use placeholders like [Course Catalog Link] unless an explicit link was provided.
- Summarize modules/outcomes/prereqs at a high level without fabricating specifics.

𝗢𝗨𝗧𝗣𝗨𝗧 𝗙𝗢𝗥𝗠𝗔𝗧 (strict)
- Optionally, first line ONLY if escalation:
  {"needs_human": true, "category": "support|billing|security|other", "confidence": 0.72}
- Then EXACTLY:
---
REPLY:
<plain text only, no HTML/Markdown>

SUBJECT:
<suggested subject line; default to “Re: {Subject}” if continuing a thread>
---

𝗣𝗥𝗢𝗛𝗜𝗕𝗜𝗧𝗜𝗢𝗡𝗦
- Do NOT invent prices, discounts, dates, URLs, or certification claims.
- Do NOT output outside the specified format.
- Do NOT include code blocks or HTML.

Now write the reply for the given ID, TO reply, Subject, and Body.
```

*(The above mirrors your JSON prompt schema and output blocks.)*

## 7) 𝗪𝗜𝗥𝗘 𝗚𝗘𝗠𝗜𝗡𝗜 → 𝗔𝗜 𝗔𝗚𝗘𝗡𝗧

Open **AI Agent → Language Model** and select the **Google Gemini Chat Model** you added in step 5.
This exact ai\_languageModel link is present in your JSON.

## 8) 𝗖𝗢𝗗𝗘 𝗜𝗡 𝗝𝗔𝗩𝗔𝗦𝗖𝗥𝗜𝗣𝗧 (Parser)

Add a **Code** node after **AI Agent**. Paste this parser (lifted from your file and trimmed for clarity). It:

* Reads the Agent’s text,
* Optional first-line JSON for `needs_human`,
* Extracts **REPLY** and **SUBJECT** blocks,
* Provides a safe subject fallback from upstream.

```javascript
// Parse the agent's output into replyText/replySubject + needs_human
const raw =
  $json.output || $json.text || $json.data ||
  $json.choices?.[0]?.message?.content || $json.choices?.[0]?.text || '';

let body = String(raw || '').trim();
const result = { replyText: '', replySubject: '', needs_human: false, raw };

// Optional first-line JSON (escalation)
const firstLine = body.split('\n',1)[0].trim();
if (firstLine.startsWith('{') && firstLine.endsWith('}')) {
  try {
    const meta = JSON.parse(firstLine);
    if (typeof meta.needs_human === 'boolean') result.needs_human = meta.needs_human;
    body = body.slice(firstLine.length).trim();
  } catch {}
}

// Extract REPLY + SUBJECT blocks
const m = body.match(/REPLY:\s*([\s\S]*?)\n+SUBJECT:\s*([\s\S]*)$/i);
if (m) {
  result.replyText = m[1].trim();
  result.replySubject = m[2].trim();
} else {
  result.replyText = body || 'Thanks for your email — could you share a few more details?';
  result.replySubject = '';
}

// Safe default subject from upstream if agent didn't supply one
const upstreamSubject = $json['Subject '] || $json.Subject || $json.subject || 'Regarding your request';
if (!result.replySubject) result.replySubject = `Re: ${upstreamSubject}`.trim();

return [{ json: result }];
```

## 9) 𝗥𝗘𝗣𝗟𝗬 𝗧𝗢 𝗔 𝗠𝗘𝗦𝗦𝗔𝗚𝗘 (Gmail)

Add **Gmail → Reply to a message** after the Code node:

* **Message/Thread**: map from the original trigger (`{{$json.id || $json.messageId || $json.threadId}}` preserved along the path).
* **To**: use `={{$json['To Reply']}}` (from Step 2).
* **Subject**: `={{$json.replySubject}}`
* **Body**: `={{$json.replyText}}`
  This mirrors the final hop in your JSON wiring.

## 10) 𝗢𝗣𝗧𝗜𝗢𝗡𝗔𝗟 — 𝗚𝗔𝗧𝗘 𝗘𝗦𝗖𝗔𝗟𝗔𝗧𝗜𝗢𝗡

Insert an **IF** node right after **Code**:

* Condition: `={{$json.needs_human}} is true`

  * **True** → route to a human-review path (e.g., create a draft, add Gmail label, or forward to support inbox).
  * **False** → continue to **Reply to a message**.

---

# 𝗥𝘂𝗻 & 𝗩𝗲𝗿𝗶𝗳𝘆

* Trigger an email → see it logged to Sheets → Agent drafts reply → Code parses → Gmail sends reply (unless escalated).
* The **strict output format**, **tone rules**, and **no-fabrication safety** come straight from your embedded prompt spec.
