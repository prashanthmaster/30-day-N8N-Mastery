# HTTP Requests — Making n8n Talk to the World (GET Only)



---

## Goal

Build a simple workflow that makes a **GET** request to a public API 

Workflow overview:
```
Manual Trigger → HTTP Request (GET) → Set (optional)
```

Expected result (example):
```json
{
  "message": "Fetched TODO successfully",
  "todo_id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

---

## Prerequisites

```text
+ n8n is running (default local URL: http://localhost:5678)
+ You can open the n8n Editor (canvas view)
+ Internet access is available
```

Key terms:
```text
+ Node  → a block that performs one task (trigger, request, format, etc.)
+ Canvas → the whiteboard area where you place and connect nodes
+ Connection → the line from one node’s output to another node’s input
```

---

## STEP 1 — Create a New Workflow  (drag‑and‑drop: not required)

### Do
```text
+ Open the n8n Editor
  → Click “New” to start a blank workflow
  → Click the Untitled name at top‑left and rename to: HTTP GET — Basic Demo
  → Click Save (or ensure Auto‑save is enabled)
```

### Verify
```text
+ You see an empty canvas
+ The left panel shows the node search and list
```

---

## STEP 2 — Add the Manual Trigger Node  (drag‑and‑drop: required)

### Do
```text
+ In the left panel search, type: Manual Trigger
  → Drag Manual Trigger onto the canvas
  → Place it near the left edge (this will be the start)
```

### Configure
```text
+ No configuration needed (defaults are fine)
```

### Verify
```text
+ The Manual Trigger node appears without warnings
```

---

## STEP 3 — Add the HTTP Request Node (GET)  (drag‑and‑drop + connection: required)

### Do
```text
+ In the left panel search, type: HTTP Request
  → Drag HTTP Request onto the canvas
  → Drop it to the right of Manual Trigger
  → Create a connection:
    + Click the small circle on the right side of Manual Trigger
    + Drag the arrow line to the left side of HTTP Request until it snaps
```

### Configure (Node configuration — key fields)
```text
+ Click the HTTP Request node to open its panel
  → HTTP Method      : GET
  → URL              : https://jsonplaceholder.typicode.com/todos/1
  → Response Format  : JSON
  → Authentication   : (leave empty for this demo)
  → Headers          : (leave empty)
  → Query Parameters : (leave empty)
```

Optional advanced (only if needed):
```text
+ Options → Timeout      → increase if API is slow
+ Options → Ignore SSL   → keep OFF unless required
```

### Test this node alone (recommended)
```text
+ Select the HTTP Request node
  → Click Execute Node (in the right panel)
  → Open the JSON output tab
  → Confirm fields like: userId, id, title, completed
```

### Troubleshoot (common quick checks)
```text
+ Non‑200 code? → Read the response body for details
+ No output?   → Re‑run; confirm internet connectivity
```

---

## STEP 4 — Add a Set Node to Format Output (optional)  (drag‑and‑drop + connection: required)

### Do
```text
+ In the left panel search, type: Set
  → Drag Set onto the canvas
  → Drop it to the right of HTTP Request
  → Connect HTTP Request → Set using the same arrow drag method
```

### Configure (Node configuration — key fields)
```text
+ Click the Set node
  → Keep Only Set  : ON
  → Add fields:
    + string   → name: message    → value: Fetched TODO successfully
    + string   → name: title      → value: ={{ $json["title"] }}
    + string   → name: completed  → value: ={{ $json["completed"] }}
    + number   → name: todo_id    → value: ={{ $json["id"] }}
```

Notes:
```text
+ The ={{ ... }} expression reads values from the previous node’s JSON
+ Keep Only Set = ON ensures only your selected fields appear in the final output
```

### Verify
```text
+ Select the Set node
  → Click Execute Node
  → Output shows only: message, todo_id, title, completed
```

---

## STEP 5 — Run the Entire Workflow

### Do
```text
+ Click Execute Workflow (top‑right)
  → Observe the execution path:
    Manual Trigger → HTTP Request → Set (if you added it)
```

### Verify
```text
+ Final output (if Set used) looks like:
  {
    "message": "Fetched TODO successfully",
    "todo_id": 1,
    "title": "delectus aut autem",
    "completed": false
  }
+ If Set not used, the HTTP Request output shows the full API response
```

---

## STEP 6 — Variant: Query Parameters (optional)

Example endpoint: https://httpbin.org/get

### Do
```text
+ Duplicate the HTTP Request node (right‑click → Duplicate) or add a new one
  → HTTP Method : GET
  → URL         : https://httpbin.org/get
  → Expand “Query Parameters”
    + Click Add Parameter
      → Name  : userId
      → Value : 1
```

### Verify
```text
+ Execute Node
  → In the JSON output, find the args section and confirm userId=1 is present
```

---

## Visual Layout (text mock diagram)

```
[Manual Trigger] → [HTTP Request (GET)] → [Set (Format)]
```

Legend:
```text
+ Square brackets [] are nodes
+ The arrow shows the connection you create by dragging from one node’s dot to the next
```

---

## Common Errors and Fixes

```text
+ 401 / 403 Unauthorized / Forbidden
  → Not expected in this demo URL; for your own API, configure Authentication in HTTP Request

+ 404 Not Found
  → Check the URL spelling or endpoint path

+ 429 Too Many Requests
  → Public API rate limit; wait and retry

+ Empty or malformed JSON
  → Ensure Response Format is JSON or use the correct endpoint

+ Network issues / firewalls
  → Verify internet access from the machine running n8n
```

---

## Summary

```text
+ Manual Trigger starts the run
+ HTTP Request (GET) retrieves data from a public endpoint
+ Set (optional) trims and formats the output for easy reading
+ Query Parameters can be added in the node without editing the raw URL
```
