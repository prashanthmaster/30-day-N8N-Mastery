# Power Pattern: Input → Process → Output (Drive → Code → Gemini → Gmail)

> **Source:** Your uploaded workflow.  
> **LLM Used:** **Gemini Chat model** (Google AI Studio)  
> **Goal:** When a new **CSV** is added to a specific **Google Drive** folder, automatically parse it, compute quick stats via a **Code** node, generate a compact **HTML** summary with **Gemini**, and **email** it using **Gmail**.

---

## 🔐 Authentication (complete these first)

- **Google Drive (OAuth2)**
  - In n8n → **Credentials** → create Google Drive OAuth2.
  - Grant file read access.
- **Gmail (OAuth2)**
  - In n8n → **Credentials** → create Gmail OAuth2.
  - Ensure **Send email** scope is allowed.
- **Gemini (Google AI Studio)**
  - In n8n → configure **LLM Chain** to use **Gemini Chat model** and your API key/credentials.

> ⚠️ Without Drive + Gmail OAuth and Gemini credentials, this workflow will not run.

---

## 🧭 High-Level Flow

**Google Drive Trigger** ➝ **Google Drive (Download)** ➝ **Extract From File** ➝ **Code (JavaScript)** ➝ **LLM Chain (Gemini)** ➝ **Gmail (Send)**

---

## 🏗️ Build It (drag → drop → configure)

### 1) Google Drive Trigger (entry)
**Add Node:** *Google Drive Trigger* → place at the left (start node)

- **Trigger On:** `File Created`  
- **Folder ID:** `YOUR_FOLDER_ID`  
  - _How to get it:_ Open the target Drive folder in your browser and copy the long ID from the URL.

**Why:** Starts the workflow whenever a file is created inside the folder.

---

### 2) Google Drive (Download file)
**Add Node:** *Google Drive*  
**Connect:** `Google Drive Trigger ➝ Google Drive (Download)`

- **Operation:** `Download`  
- **File ID:**  
  ```n8n
  ={{ $json["id"] }}
  ```
- **Binary Property Name:** `data`

**Why:** Retrieves the actual file bytes for parsing.

---

### 3) Extract From File
**Add Node:** *Extract From File*  
**Connect:** `Download ➝ Extract From File`

- **Operation:** `Extract`  
- **Binary Property Name:** `data`  
- **File Format:** `Auto` (works well for CSV; you may set explicitly if needed)

**Why:** Converts the CSV into JSON rows for downstream processing.

---

### 4) Code (JavaScript)
**Add Node:** *Code*  
**Connect:** `Extract From File ➝ Code (JavaScript)`  
**Parameters:**

- **Language:** `JavaScript`  
- **Code:** _(copy-paste exactly)_
```javascript
const rows = items.map(i => i.json);
const rowCount = rows.length;

if (rowCount===0){
  return [{json:{summaryContext:'No rows found.',columns:[],rowCount:0}}];
}

const columns = Object.keys(rows[0]);
const numericCols = columns.filter(c =>
  rows.every(r => r[c]==null || r[c]==='' || !isNaN(Number(r[c])))
);

const stats = {};
for (const c of numericCols){
  const nums = rows.map(r => Number(r[c])).filter(v => !isNaN(v));
  if(nums.length){
    const sum = nums.reduce((a,b)=>a+b,0);
    stats[c] = {
      count: nums.length,
      min: Math.min(...nums),
      max: Math.max(...nums),
      mean: Number((sum/nums.length).toFixed(2))
    };
  }
}

const sample = rows.slice(0,10);

const summaryContext = {
  meta: { rowCount, columns, numericColumns: numericCols },
  quickStats: stats,
  sampleRows: sample
};

return [{
  json:{
    columns,
    rowCount,
    summaryContext: JSON.stringify(summaryContext, null, 2)
  }
}];
```

**What it does:**  
- Counts rows, lists columns  
- Detects numeric columns  
- Computes **min / max / mean** per numeric column  
- Packs everything as a JSON string in `summaryContext` for the LLM

---

### 5) LLM Chain (Gemini)
**Add Node:** *LLM Chain*  
**Connect:** `Code ➝ LLM Chain (Gemini)`  
**Parameters:**

- **Provider/Model:** `Gemini` (**Chat model**)  
- **Prompt Type:** `Plain`  
- **Prompt (copy-paste exactly):**
```text
You are a precise data analyst. Produce a compact, Gmail-friendly HTML summary of a CSV dataset.

HARD RULES
- DO NOT include a “Columns and Data Types” (or any schema) section.
- Sections must be exactly, in this order: Overview, Key Metrics, Notable Insights, Next Steps.
- Use only inline styles. Neutral grays only (#111 text, #555 muted, #e5e7eb borders). No external CSS/JS.
- Keep output under ~250 words. No apologies or meta commentary.

INPUT
The variable {{ $json.summaryContext }} is a JSON string containing:
- meta.rowCount, meta.columns, meta.numericColumns
- quickStats: for each numeric column → {count, min, max, mean}
- sampleRows: up to 10 example rows

WHAT TO WRITE
1) Overview...
2) Key Metrics...
3) Notable Insights...
4) Next Steps...

OUTPUT (return only this single HTML block; no <html> or <body> tags):
<div style="font-family:Arial,Helvetica,sans-serif;color:#111;line-height:1.6;font-size:14px;">
  <h3 style="margin:0 0 8px 0;color:#111;">Overview</h3>
  <h3 style="margin:16px 0 8px 0;color:#111;">Key Metrics</h3>
  <h3 style="margin:16px 0 8px 0;color:#111;">Notable Insights</h3>
  <ul style="margin:0 0 12px 18px;padding:0;"></ul>
  <h3 style="margin:16px 0 8px 0;color:#111;">Next Steps</h3>
  <ul style="margin:0;padding:0 0 4px 18px;"></ul>
</div>
```

**Why:** Uses Gemini to transform `summaryContext` into a professional, compact HTML block suitable for Gmail.

---

### 6) Gmail (Send)
**Add Node:** *Gmail*  
**Connect:** `LLM Chain (Gemini) ➝ Gmail (Send)`  
**Parameters:**

- **Operation:** `Send`  
- **To (To List):** `you@example.com` → replace with your recipient(s)  
- **Subject:**
  ```n8n
  ={{ "CSV Summary — " + $json.rowCount + " rows" }}
  ```
- **Message:**
  ```n8n
  ={{ $json.text }}
  ```
- **Options → Send As HTML:** `true`

**Why:** Emails the LLM-generated HTML summary with a clear subject.

---

## ▶️ Test

1. Click **Execute Workflow (Test)**.  
2. Upload a CSV to the watched Drive folder.  
3. Verify:
   - **Extract From File** outputs JSON rows.  
   - **Code** shows `rowCount`, `columns`, `summaryContext`.  
   - **LLM Chain** returns a single HTML block in `text`.  
   - **Gmail** sends a formatted email: _“CSV Summary — N rows”_.

---

## 🚀 Deploy

- Toggle workflow **Active** to run on the **Production** trigger.  
- Any new CSV in the folder triggers the email flow automatically.

---

## 📦 Copy-Paste Snippets

### A) Code Node (JS)  
> Already provided in step 4 — paste as-is.

### B) Gemini Prompt (LLM Chain)  
> Already provided in step 5 — paste as-is.

### C) Subject Template
```n8n
={{ "CSV Summary — " + $json.rowCount + " rows" }}
```

### D) HTML Body (from LLM)
```n8n
={{ $json.text }}
```
> Make sure **Send As HTML** is enabled in the Gmail node.

---

## 🧩 Notes & Tips

- **CSV Variants:** “Auto” format works for CSV; for TSV/XLSX, set appropriately if needed.  
- **Non-numeric fields:** Safely skipped in stats; only numeric columns get min/max/mean.  
- **Multiple recipients:** Add more emails in the Gmail node’s To list.  
- **HTML safety:** Inline-only styles keep Gmail rendering consistent.

---

## 🛠️ Troubleshooting

- **No email received:** Check Gmail credentials/scope, ensure “Send As HTML” is true, review execution logs.  
- **LLM error:** Verify Gemini credentials and that the model is set to **Chat**.  
- **Trigger silent:** Confirm **Folder ID** and that files are being **created** (not just edited).  
- **Empty stats:** Your numeric columns may contain text — clean input or adapt the Code node.

---

## ✅ What You Have Now

- A robust **Drive → Code → Gemini → Gmail** pipeline  
- Copyable **Code node** and **Prompt**  
- Clear deployment/testing steps

> Want this as a ready-to-import **Workflow.json** too? Ask and I’ll generate it next.
