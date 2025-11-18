# Email Connections — n8n Form → Gmail (Schema-Driven, No Webhook)



---

## Goal

When someone submits an **n8n Form**:
- Capture inputs using **Form Trigger** (path `forms/contact`).
- Send an email using **Gmail** with subject and message from the form.

**Flow (text mockup)**
```
[Form Trigger] → [Gmail: Send a message]
```

---

## Prerequisites

```text
+ n8n running (local editor: http://localhost:5678 or your hosted URL)
+ Gmail account you control
+ n8n credential: Gmail OAuth2 (configured in n8n → Credentials → Gmail OAuth2)
```

**Gmail OAuth2 quick setup**
```text
+ Google Cloud Console:
  → Create project → Enable “Gmail API”
  → OAuth consent screen: External → add yourself as Test user
  → Create OAuth Client ID (Web application)
  → Authorized redirect URI:
    https://<your-n8n-host>/rest/oauth2-credential/callback
+ In n8n Credentials → “Gmail OAuth2”:
  → Paste Client ID & Secret → Connect OAuth2
```

---

## Step-by-Step (with sub-steps)

### STEP 1 — Form Trigger (collect inputs)  (drag-and-drop: required)

#### Do
```text
+ Left panel search: Form Trigger
  → Drag to canvas (leftmost)
  → Click to configure
```

#### Configure (match schema exactly)
```text
+ Path            : forms/contact
+ Form Title      : Contact Us
+ Description     : sample mail from
+ Fields (Add Field for each):
  → Name
    + Type        : Text
    + Placeholder : Enter a name
    + Required    : ON
  → Email
    + Type        : Email
    + Placeholder : Enter your email 
    + Required    : ON
  → Mail Subject
    + Type        : Textarea
    + Placeholder : Enter a Subject
    + Required    : ON
  → Message
    + Type        : Textarea
    + Placeholder : Enter short message body 
    + Required    : ON
```

#### Notes
```text
+ Click “Execute workflow” to enable the Test form URL
+ Use “Open form” in the node to preview and submit
+ Output JSON keys match field labels exactly:
  Name, Email, Mail Subject, Message
```

---

### STEP 2 — Gmail “Send a message”  (drag-and-drop + connection: required)

#### Do
```text
+ Left panel search: Gmail
  → Drag “Send a message” to the canvas (right of Form Trigger)
  → Connect: Form Trigger → Send a message
```

#### Configure (node configuration — key fields)
```text
+ Credentials        : Gmail OAuth2 (select your connected credential)
+ Operation          : Send
+ To                 : ={{ $json.Email }}
+ Subject            : ={{ $json['Mail Subject'] }}
+ Email Type         : Text
+ Message            : ={{ $json.Message }}
+ Options
  → Append n8n Attribution : ON or OFF (your choice)
```

**Expression mapping cheat-sheet**
```text
To       → ={{ $json.Email }}
Subject  → ={{ $json['Mail Subject'] }}
Message  → ={{ $json.Message }}
```

---

## Run and Verify

```text
+ Save the workflow
+ Click Execute workflow (top-right)
+ Click “Open form” on Form Trigger → fill and submit
+ The Gmail node should turn green; check the recipient inbox
```

---

## Troubleshooting

```text
+ “Access blocked” or 403 in Gmail:
  → Add yourself as Test user in Google OAuth consent screen
  → Reconnect Gmail OAuth2 in n8n

+ Email not delivered:
  → Verify “To” mapping (= {{ $json.Email }})
  → Try another recipient; check spam

+ Form not loading:
  → Click Execute workflow for Test URL
  → Toggle workflow Active for the Production URL
```


