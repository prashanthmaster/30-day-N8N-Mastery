# HTTP POST — Basic Demo (n8n)
One‑line goal: Send a JSON payload from n8n to a public test API, then format a clean response.

## At‑a‑glance outcomes
- Build a JSON body with **Set** → POST it with **HTTP Request** → prettify output with **Set**.  
- Learn the exact **jsonParameters** + `={{ $json }}` pattern for POSTing clean JSON.  
- Get a predictable “saved (simulated)” response you can reuse in bigger flows.

## Prereqs & Auth (do this first)
- **n8n**: Cloud or self‑hosted (any recent version).  
- **Public URL / HTTPS**: Not required for this manual demo.  
- **API keys**: **None** needed. We use **JSONPlaceholder** (mock API).  
  - Note: It **simulates** persistence and always returns a fake `id`. Good for testing only.

## Architecture snapshot (nodes & tools)
1) **Manual Trigger** (`id: 1`)  
2) **Set (Build Payload)** (`id: 2`) → creates `name`, `note`, `priority`, `category`  
3) **HTTP Request (POST)** (`id: 3`) → POST to a mock API, body = `={{ $json }}`  
4) **Set (Format Response)** (`id: 4`) → returns `message`, `echoed_name`, `echoed_note`, `post_id`  

---

## Step‑by‑Step

### 1) Create the workflow
➜ a. Click **+ New** → add **Manual Trigger**.  
➜ b. Rename to **Manual Trigger** (optional).  
➜ c. **Save**.

### 2) Build the payload (**Set** node)
➜ a. Add a **Set** node; name it **Set (Build Payload)**.  
➜ b. In **Mode**, keep **Keep Only Set** = **ON**.  
➜ c. Under **Values → String**, add four rows:  
   - **name** → `Asha`  
   - **note** → `Here's some data to save`  
   - **priority** → `high`  
   - **category** → `onboarding`  
➜ d. **Save**.  
*Ref: images/02-set-payload.png*

**Key parameters (Set — Build Payload)**

| Field | Value |
|---|---|
| Keep Only Set | **ON** |
| Strings | name=`Asha`, note=`Here's some data to save`, priority=`high`, category=`onboarding` |

### 3) Send the POST (**HTTP Request**)
➜ a. Add **HTTP Request**; name it **HTTP Request (POST)**.  
➜ b. **Method** → **POST**.  
➜ c. **URL** → `https://jsonplaceholder.typicode.com/posts`  
➜ d. Toggle **Send Body as JSON / jsonParameters** → **ON**.  
➜ e. **Body Parameters (JSON)** → use expression **exactly**: `={{ $json }}`  
➜ f. **Send Binary Data** → **OFF**.  
➜ g. **Save**.  
*Ref: images/03-http-post.png*

**Key parameters (HTTP Request)**

| Field | Value |
|---|---|
| Request Method | **POST** |
| URL | `https://jsonplaceholder.typicode.com/posts` |
| jsonParameters | **ON** |
| Body Parameters (JSON) | `={{ $json }}` |
| Send Binary Data | **OFF** |

### 4) Format the output (**Set** node)
➜ a. Add another **Set**; name it **Set (Format Response)**.  
➜ b. **Keep Only Set** = **ON**.  
➜ c. **Strings**:  
   - **message** → `Saved successfully (simulated)`  
   - **echoed_name** → `={{ $json["name"] }}`  
   - **echoed_note** → `={{ $json["note"] }}`  
➜ d. **Number**:  
   - **post_id** → `={{ $json["id"] }}`  
➜ e. **Save**.  
*Ref: images/04-format-response.png*

**Key parameters (Set — Format Response)**

| Field | Value |
|---|---|
| Keep Only Set | **ON** |
| Strings | message=`Saved successfully (simulated)`, echoed_name=`={{ $json["name"] }}`, echoed_note=`={{ $json["note"] }}` |
| Number | post_id=`={{ $json["id"] }}` |

### 5) Connect nodes (in order)
**Manual Trigger** → **Set (Build Payload)** → **HTTP Request (POST)** → **Set (Format Response)**.  
*Ref: images/01-canvas.png*

---

## Testing & validation
1) Open the workflow → click **Execute Workflow**.  
2) Inspect **HTTP Request (POST)** → **Output** should show your payload plus a new `id`.  
3) Inspect **Set (Format Response)** → you should see a clean summary with `message`, `echoed_*`, `post_id`.  
4) Change **Set (Build Payload)** values (e.g., name=`Ravi`) → run again → verify changes flow through.

**Notes**
- This is a **manual** run. No webhook/activation required.  
- Asia/Kolkata (IST) timezone doesn’t affect this demo (no dates involved).

---

## Troubleshooting (top fixes)
- **Wrong body / empty body** → Ensure **jsonParameters = ON** and **Body Parameters (JSON)** is `={{ $json }}` (expression, not a quoted string).  
- **Expression shows as a string** → Remove quotes; it must render **purple** in n8n.  
- **Unexpected fields** → Confirm you used **Keep Only Set = ON** in both **Set** nodes.  
- **404 or 405** → Double‑check URL and **POST** method.  
- **ECONNREFUSED / network error** → Check internet/DNS; try again or test URL in a browser.  
- **Undefined key in Format node** → Make sure the key names (`name`, `note`) match the response shape from the HTTP node.

---

## What to deliver (repo checklist)
- Short summary of purpose (one paragraph).  
- Node list with order and key parameters (tables above).  
- Screenshots (optional):  
  - images/01-canvas.png — full workflow  
  - images/02-set-payload.png — Set (Build Payload)  
  - images/03-http-post.png — HTTP Request config  
  - images/04-format-response.png — Set (Format Response)  
