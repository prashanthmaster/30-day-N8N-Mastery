# **MongoDB Memory (Permanent Chat Memory) — n8n AI Agent Guide**

This walkthrough is laser-focused on **MongoDB as the memory store** so your **AI Agent can remember every previous chat permanently**. It’s written for someone totally new to n8n, and it mirrors the structure of your uploaded workflow (same node names, wiring, and key settings). 
---

## What you’ll build (at a glance)

**Flow (nodes in order):**  
**When chat message received** → **AI Agent**  
…and the **AI Agent** connects to:  
- **OpenAI Chat Model** (LLM brain)  
- **MongoDB Chat Memory** (permanent memory store)

This wiring lets the Agent pull **past conversation turns** from MongoDB before replying, then keep storing the new turns for next time. 

--- 
![Canvas](images/canvas.png)

---

## MongoDB-first Prerequisites

1) **MongoDB deployment**
   - **MongoDB Atlas** (recommended) or self-hosted MongoDB 6.x+.
   - Create a **database user** with `readWrite` on your memory database (guide assumes `n8n-memory`).
   - **Network Access / IP Allowlist**: add your n8n server’s IP (or “allow from anywhere” for testing).
   - Keep the **connection string** handy, e.g.  
     `mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/`

2) **n8n credentials**
   - **MongoDB account** (use the URI above, plus username/password).
   - **OpenAI API** (your OpenAI key).

3) **n8n instance** (Cloud or Desktop) with access to the internet (for OpenAI) and to your MongoDB cluster.

---

## Node-by-Node Build (original names + what to click)

> The node names and key values below match your JSON: **databaseName** `n8n-memory`, **contextWindowLength** `15`, **model** `gpt-4`, and the exact wiring (language model & memory ports into the Agent).

### 1) **When chat message received**  
*Type:* `@n8n/n8n-nodes-langchain.chatTrigger`  
**Why:** Starts the workflow whenever a chat message arrives (from Chat UI/webhook).

**Steps**
1. Drag **When chat message received** to the canvas.  
2. No extra config needed for this guide.

**Wire:** **When chat message received → AI Agent** (main output to main input). 

---

### 2) **OpenAI Chat Model**  
*Type:* `@n8n/n8n-nodes-langchain.lmChatOpenAi`  
*Model (from your JSON):* `gpt-4` fileciteturn9file0

**Steps**
1. Drag **OpenAI Chat Model** onto the canvas.  
2. Select your **OpenAI API** credential.  
3. Choose **Model = gpt-4** (or an available chat model).

**Wire:** **OpenAI Chat Model → AI Agent** using the Agent’s **ai_languageModel** port (the small model port under the Agent). fileciteturn9file0

---

### 3) **MongoDB Chat Memory** (the star of the show)  
*Type:* `@n8n/n8n-nodes-langchain.memoryMongoDbChat`  
*Key params (from your JSON):*  
- **Database Name:** `n8n-memory`  
- **Context Window Length:** `15` (how many turns the Agent pulls each time) 

**Steps**
1. Drag **MongoDB Chat Memory** onto the canvas.  
2. Set **Database Name** = `n8n-memory`.  
3. Set **Context Window Length** = `15` (tune as you like: larger = more context reads).  
4. In **Credentials**, pick your **MongoDB account** (URI + user/pass).

**Wire:** **MongoDB Chat Memory → AI Agent** via the Agent’s **ai_memory** port (the small memory port).  
This gives the Agent **permanent, queryable conversation memory** in MongoDB across sessions. fileciteturn9file0
---
![Database](images/Mongodb.png)
---

### 4) **AI Agent**  
*Type:* `@n8n/n8n-nodes-langchain.agent`  
*Prompt Type:* `Define` (we’ll paste the system prompt below) 

**What this node does**  
- Receives the **new user message** from the trigger.  
- Pulls **prior turns** from **MongoDB Chat Memory** (using the port).  
- Uses **OpenAI Chat Model** to reason and respond, grounded in the pulled history.  
- Returns a final text output.

**Steps**
1. Drag **AI Agent** onto the canvas.  
2. Set **Prompt Type** = `Define`.  
3. **Paste the System Prompt (below)** into the **AI Agent**’s prompt box.

#### Paste this **System Prompt** (right below the AI Agent node)

```text
# System Prompt — Permanent MongoDB Memory

ROLE
You are a helpful, friendly AI assistant with permanent chat memory stored in MongoDB.
Before replying, you always incorporate prior turns from MongoDB Chat Memory.

MEMORY RULES
- Treat the MongoDB Chat Memory as source of truth for past turns.
- If memory is present, summarize the relevant parts to stay concise but accurate.
- If there is no prior memory, proceed as a first message and establish context.
- Do not fabricate prior messages; rely only on the memory provided by the system.

OBJECTIVE
Given the current user message and the loaded MongoDB memory (last N turns),
produce a clear, helpful, and accurate reply that respects previous context.

STYLE
- Warm, professional, concise.
- Ask a single clarifying question if the user’s request is ambiguous.

SAFETY
- If you don’t know, say so briefly and suggest a next best step.

OUTPUT
- Return ONLY the final reply text (no JSON or extra keys).
```

> This replaces the simpler default prompt in your JSON with one that **explicitly instructs the Agent to rely on MongoDB memory** every time. (Your JSON shows an Agent with `promptType: "define"` already set and wired to both **OpenAI Chat Model** and **MongoDB Chat Memory**.) fileciteturn9file0

---

## Verify the wiring (matches your JSON)

- **When chat message received → AI Agent** (main connection)  
- **OpenAI Chat Model → AI Agent (ai_languageModel)**  
- **MongoDB Chat Memory → AI Agent (ai_memory)**

And the MongoDB memory node uses:  
- **databaseName:** `n8n-memory`  
- **contextWindowLength:** `15`  
The model node uses **gpt-4**.

---

## How permanence works (MongoDB mental model)

- Each conversation/thread is **identified by the chat runtime** (n8n passes the identifier to the memory component under the hood).  
- The **MongoDB Chat Memory** node writes new turns and reads **the last N** (your **Context Window Length**) on each message.  
- Because it sits in **MongoDB**, the memory **persists indefinitely**—survives restarts, deployments, and new sessions—until you purge it.

> If you want even longer recall, raise the **Context Window Length**. Keep in mind bigger windows means more tokens/context per reply.

---

## First end-to-end test

1) Trigger a message (“Hi, remember my favorite color is teal”).  
2) Bot replies and **stores the turn** in MongoDB.  
3) Send another message in the **same chat** (“What’s my favorite color?”).  
4) Bot should answer using **prior memory** (“You said it’s teal”), proving permanent recall.

---

## Troubleshooting (Mongo-focused)

- **Authentication/Network errors**  
  - Re-check the **MongoDB URI** and user/password.  
  - In Atlas, add your server IP to **Network Access**.  
- **No recall between messages**  
  - Ensure **MongoDB Chat Memory** is connected to the Agent’s **ai_memory** port.  
  - Confirm the chat messages are in the **same thread/session** (the chat frontend should maintain this).  
  - Increase **Context Window Length** if you’re not seeing enough past turns.  
- **Model not responding**  
  - Verify **OpenAI API** credential and model availability.  
  - Ensure the **ai_languageModel** port is connected from **OpenAI Chat Model** to **AI Agent**.  
- **Performance**  
  - Very large histories can grow over time; the memory node only fetches the last **N turns** you configured. Raise or lower N as needed.

---

## Why MongoDB for memory?

- **Durable**: data survives restarts and deploys.  
- **Scalable**: handles growth far better than a spreadsheet or in-memory store.  
- **Queryable**: you can inspect or export conversations for analytics and improvements.
---
![Database](images/output.png)
---

### You’re done 🎉

You now have an **AI Agent with permanent MongoDB memory**: the Agent reads past turns before answering and keeps writing new turns back for the next time—**exactly how your JSON is wired** (Agent + OpenAI Chat Model + MongoDB Chat Memory, with `n8n-memory` DB and context window 15). 

If you want, I can also export this guide as a **PDF** or extend it to support **conversation resets**, **user-level namespaces** (separate memory per user), or **selective forgetting** flows.
