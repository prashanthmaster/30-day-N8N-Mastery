#  AND & OR Logic Workflow — n8n

---

##  Goal

Learn how to use **AND** and **OR** conditions with the **If Node** in n8n.  
- Start with a **Manual Trigger**.  
- Add values and test conditions:  
  - **Condition 1 (AND):** Check if `Age > 18` **AND** `Country = "India"`.  
  - **Condition 2 (OR):** Check if `Score > 80` **OR** `Rank < 10`.  

---

##  Step-by-Step Demo

### Step 1: Add Manual Trigger
- Drag in a **Manual Trigger Node**.  
- No config needed.  

---

### Step 2: Add an If Node (AND Condition)
- Connect **Manual Trigger ➝ If (AND)**.  
- Configure:
  - **Condition 1:** `Age > 18`  
  - **Condition 2:** `Country = India`  
  - Select **Combine Conditions with: AND**  

➡️ This checks if **both conditions are true**.

---

### Step 3: Handle AND Results
- From **True output** → Add a Set Node:
```json
{ "message": " User is an adult AND from India" }
```
- From **False output** → Add a Set Node:
```json
{ "message": " Condition failed (either not adult or not from India)" }
```

---

### Step 4: Add another If Node (OR Condition)
- From **Manual Trigger** (add second branch), connect to a new **If Node (OR)**.  
- Configure:
  - **Condition 1:** `Score > 80`  
  - **Condition 2:** `Rank < 10`  
  - Select **Combine Conditions with: OR**  

➡️ This checks if **any one condition is true**.

---

### Step 5: Handle OR Results
- From **True output** → Add a Set Node:
```json
{ "message": " Qualified by score or rank" }
```
- From **False output** → Add a Set Node:
```json
{ "message": " Did not qualify" }
```

---

##  Mock Diagram

```
Manual Trigger
     ⬇
 ┌──────────────┐
 │ If (AND)     │
 │ Age > 18 AND │
 │ Country=India│
 └─────┬────────┘
   T ✅│          F ❌
       ⬇             ⬇
   Set Node        Set Node
   (Adult+India)   (Failed)

Manual Trigger
     ⬇
 ┌──────────────┐
 │ If (OR)      │
 │ Score>80 OR  │
 │ Rank<10      │
 └─────┬────────┘
   T 🏆│          F ❌
       ⬇             ⬇
   Set Node        Set Node
   (Qualified)     (Not qualified)
```

---

##  Importable JSON

See the provided **demo.json** file for direct import in n8n.

---

##  Key Takeaway

 **AND** = All conditions must be true.  
 **OR** = Any one condition is enough.  
