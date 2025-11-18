#  n8n — Set Node Mastery: Transform, clean, and enhance

One‑line goal: Clean messy contact‑form data, validate email & phone, route with **IF (AND)**, and append valid rows to Google Sheets.

## At‑a‑glance outcomes
- Title‑case **name**, lowercase **email**, E.164 **phone**, trimmed **message**.
- Adds: `emailDomain`, `maskedEmail`, `messageLength`, `timestamp`, `tags[]`.
- **Boolean** flags: `isValidEmail`, `isValidPhone`. IF uses **AND**.
- True path → Google Sheets append; False path → NoOp (or alert).

## Prereqs & Auth
- No auth for Manual Trigger / Set / IF / NoOp.
- **Google Sheets OAuth2** (n8n):
  ➜ a. **Credentials → New → Google Sheets OAuth2 API**  
  ➜ b. Google Cloud Console → OAuth client (**Web application**).  
  ➜ c. Authorized redirect: `https://YOUR_N8N_DOMAIN/rest/oauth2-credential/callback`  
  ➜ d. Scopes: `https://www.googleapis.com/auth/spreadsheets`, `https://www.googleapis.com/auth/drive.readonly`  
  ➜ e. Paste Client ID/Secret in n8n → **Connect**.  
  ➜ f. n8n **Settings → Public URL** must be your HTTPS domain.

## Architecture snapshot
1) **Manual Trigger**  
2) **Sample Input (Set)**  
3) **Clean & Enhance (Set)**  
4) **Valid? (IF)** — AND both flags  
 • **true** → **Append row in sheet (Google Sheets)**  
 • **false** → **No Operation, do nothing**

## Step‑by‑Step
### 1) Manual Trigger
➜ a. Drag **Manual Trigger** → no settings.

### 2) Sample Input (Set)
➜ a. Drag **Set** → rename **Sample Input (Set)**  
➜ b. Add Strings:  
   - `fullName` = `Enter Your name`  
   - `email`    = ` USER@Example.COM `  
   - `phone`    = `+91-93980 40588`  
   - `message`  = `Enter a message here`  
➜ c. Click **Execute node**.

### 3) Clean & Enhance (Set)
➜ a. Drag **Set** → rename **Clean & Enhance (Set)**  
➜ b. Add **String** (click **fx**):
- **name**
```js
={{ ($json.fullName || '').trim().toLowerCase().split(/\s+/).map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(' ') }}
```
- **email**
```js
={{ ($json.email || '').trim().toLowerCase() }}
```
- **emailDomain**
```js
={{ ($json.email || '').trim().toLowerCase().split('@')[1] || '' }}
```
- **phone** (E.164 IN – simple)
```js
={{ (()=>{ const d = ($json.phone || '').replace(/\D/g,''); if(!d) return ''; if(d.startsWith('91')) return '+'+d; if(d.length===10) return '+91'+d; return '+'+d; })() }}
```
- **message**
```js
={{ ($json.message || '').trim() }}
```
- **messageLength**
```js
={{ (($json.message || '').trim()).length }}
```
- **maskedEmail**
```js
={{ (()=>{ const e = ($json.email||'').trim().toLowerCase(); const [u,d]=e.split('@'); if(!u||!d) return ''; return u[0]+'***@'+d; })() }}
```
- **timestamp**
```js
={{ $now.toISO() }}
```

➜ c. Add **Boolean** (not String):
- **isValidEmail**
```js
={{ /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(($json.email||'').trim()) }}
```
- **isValidPhone**
```js
={{ (($json.phone||'').replace(/\D/g,'').length) >= 10 }}
```

### 4) IF — Valid?
**Method A (simple):**
- Condition 1 → **Value 1 (fx)** `={{ $json.isValidEmail }}` → **is true**  
- Condition 2 → **Value 1 (fx)** `={{ $json.isValidPhone }}` → **is true**  
- **Combine conditions:** **All** (AND)

**If flags are strings**: enable **Convert types where required** OR use:
```js
={{ (String($json.isValidEmail).toLowerCase()==='true') && (String($json.isValidPhone).toLowerCase()==='true') }}
```

### 5) Google Sheets (true path)
- **Operation:** Append  
- **Document:** select by URL  
- **Sheet name:** `Sheet1` (or your tab)  
- **Map columns:** `NAME, EMAIL, PHONE, MESSAGE, TIME` → from `$json`

## Testing & Validation
➜ a. Run **Sample Input → Clean & Enhance** (flags should be true/false booleans).  
➜ b. Run workflow → expect **true** path to append row.  
➜ c. Break it (bad email/short phone) → expect **false** path to NoOp.

## Troubleshooting
- “expected boolean” → store flags as **Boolean** or cast in IF.  
- No row → check IF **AND** + credentials.  
- Column mismatch → fix headers exactly.  
- Expressions not running → ensure **fx** is on.

## What to Deliver
- Working flow (Manual → Set → Set → IF → Sheets/NoOp).  
- Booleans for validity. No type errors. Appends on true.
