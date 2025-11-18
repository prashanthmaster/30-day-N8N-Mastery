# Basic If / Else Workflow in n8n

##  Goal
Create a simple workflow:
- Start with a **Manual Trigger**.
- Compare two numbers using an **If Node**.
- If **Value1 > Value2** → Go to **True Path**.
- Else → Go to **False Path**.

---

##  Step-by-Step Guide

### 1️⃣ Add Trigger Node
➡️ In the n8n editor, click **+**  
➡️ Search **Manual Trigger**  
➡️ Place it as the first node

---

### 2️⃣ Add If Node
➡️ Click **+** ➝ Add **If** node  
➡️ Connect **Manual Trigger ➝ If**  

⚙️ Configure condition:
- **Value 1:** `={{5}}`  
- **Operation:** `#Number -> is grater than`  
- **Value 2:** `={{2}}`

(Here we just use fixed numbers for clarity)

---

### 3️⃣ Add True Path Node
➡️ From **If ➝ True output**, add a **Set Node**  
➡️ Inside Set Node add:
  
     Name = message
     Value =  ✅ Value1 is greater

---

### 4️⃣ Add False Path Node
➡️ From **If ➝ False output**, add a **Set Node**  
➡️ Inside Set Node add:

     Name = message
     Value =  ❌ Value2 is greater or equal


---

## 🔄 Workflow Flow (Mock Diagram)

```
Manual Trigger
      ⬇
      If (check 2 > 5 ?)
     ↙        ↘
 True ✅      False ❌
  ⬇             ⬇
 Set Node     Set Node
  (message)    (message)
```

---

## ▶️ Run the Workflow
1. Click **Execute Workflow**.  
2. See which branch runs:  
   - If condition is **true** → message = `"✅ Value1 is greater"`  
   - Else → message = `"❌ Value2 is greater or equal"`

---


## 📝 Key Takeaway
👉 **Manual Trigger starts the workflow**  
👉 **If Node checks a condition**  
👉 **True/False branches give different outputs**  
