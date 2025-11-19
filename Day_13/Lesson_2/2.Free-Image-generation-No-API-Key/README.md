# Image-from-Chat → Google Drive (n8n) — Ultra‑Clear README

## GOAL
Turn a user’s **chat message** into an **AI-generated image** and **upload it to Google Drive** automatically.

**Pipeline:** Chat Prompt → Generate Image (pollinations.ai) → Upload to Google Drive

---

## PREREQUISITES

### Required Accounts & Tools
- **n8n** (Cloud or self-hosted) with access to the editor.
- **Google Account** with **Google Drive**.
- **Google Drive OAuth2 credential in n8n** named **exactly**: `Google Drive account` (this must exist and be authorized in *Credentials*).
- No API key is required for **pollinations.ai** (public image generation endpoint).

### Recommended n8n Node Versions
- **Chat Trigger**: `@n8n/n8n-nodes-langchain.chatTrigger` (v1.3 or later)
- **HTTP Request**: `n8n-nodes-base.httpRequest` (v4.2 or later)
- **Google Drive**: `n8n-nodes-base.googleDrive` (v3 or later)

> If you prefer to **import** instead of building manually, you can use the provided workflow JSON in this project (File → *Import from File* in the n8n editor).

---

## CANVAS WIRING (Drag‑and‑Drop Guide)

```
When chat message received  →  HTTP Request (pollinations.ai)  →  Upload to N8N Folder (Google Drive)
```

**Exact Node Names (as used in the workflow):**
1) `When chat message received`
2) `pollinations.ai`
3) `Upload to N8N Folder`

---

## WORKFLOW STEPS

### 1) Chat Trigger — “When chat message received”
**Type:** `@n8n/n8n-nodes-langchain.chatTrigger` (v1.3)  
**Purpose:** Listens for a chat message and exposes it as `chatInput` for downstream nodes.

**How to add:**
1. In the n8n editor, click **Add node** → **AI** → **Chat Trigger**.
2. Keep the defaults. The node emits a field named `chatInput` which contains the user’s message.

**What you should see when it runs:** An execution with JSON that includes a `chatInput` string (e.g., `"a watercolor fox in a misty forest"`).

---

### 2) HTTP Request — “pollinations.ai”
**Type:** `HTTP Request` (v4.2)  
**Purpose:** Calls the Pollinations image endpoint with the user’s prompt to generate an image.

**How to add:**
1. Click **Add node** → **HTTP Request**.
2. **Method:** `GET`
3. **URL:** (copy‑paste exactly; it uses the chat message as the prompt)
   ```
   =https://image.pollinations.ai/prompt/{{ $json.chatInput }}
   ```
4. Expand **Response** options and set:
   - **Response Format:** `File`
   - **Binary Property:** `data`

**Why this matters:** We need the image as **binary** so the next node can upload it to Google Drive.

**Expected output:** The node will produce a **binary** item under the property `data` (usually with a detected file extension like `.png` or `.jpg`).

---

### 3) Google Drive — “Upload to N8N Folder”
**Type:** `Google Drive` (v3)  
**Purpose:** Uploads the generated image into your Google Drive.

**How to add:**
1. Click **Add node** → **Google** → **Google Drive**.
2. **Credentials:** choose **`Google Drive account`** (must already be created & authorized in **Credentials**).
3. **Resource:** `File`
4. **Operation:** `Upload`
5. **Binary Data:** turn **ON**
6. **Binary Property:** set to:
   ```
   data
   ```
7. **Drive:** `My Drive`
8. **Folder:** `root` (or select your desired folder)

**Optional (nice to have):** Give files a readable name using the **File Name** field:
```
={{ ($json.chatInput || "image").replace(/\s+/g, "_") + ".png" }}
```
> If extension detection is important, you can leave it blank and let Google Drive accept the incoming filename, or compute it from the HTTP response headers using an Expression/Function node in more advanced flows.

---

## RUN & TEST

1) **Activate** or **Execute** the workflow in n8n.
2) Send a message to the **Chat Trigger** (e.g., via the Test Chat/trigger UI, depending on how your environment exposes it).  
   **Sample prompts:**
   - `A watercolor fox in a misty forest at dawn`
   - `A cinematic cyberpunk skyline at night`
   - `An astronaut riding a horse on Mars, ultra‑wide`
3) Watch the execution path: **Chat Trigger → HTTP Request → Google Drive**.
4) Open your Google Drive and verify the uploaded image file in the folder you configured.

---

## IMPORTING THE PROVIDED JSON (Alternative to manual build)

1) Open your n8n editor.  
2) Top‑left menu: **Workflows** → **Import from File**.  
3) Select the workflow JSON included with this README.  
4) Open the imported workflow, set the **Google Drive credential** to `Google Drive account`, and **Execute** or **Activate**.

---

## WHAT THIS WORKFLOW DOES (In Plain English)
- It **listens** for a chat message.  
- It **turns** that message into an **image** using `pollinations.ai`.  
- It **uploads** the image to your **Google Drive**—fully automated.

That’s it. A compact prompt‑to‑image‑to‑Drive automation you can extend (e.g., send the Drive link back to the chat, post to Slack, or archive filenames in a Google Sheet).
