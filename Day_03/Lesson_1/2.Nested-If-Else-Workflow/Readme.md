#  Nested If / Else Workflow — n8n

---

##  **Goal**

Use nested **If Nodes** to check conditions step by step:  

1. Start with a **Manual Trigger**.  
2. First check: **Is Value1 > Value2?**  
   * If **False** → End with message `Value2 is greater or equal`.  
   * If **True** → go deeper to a second If.  
3. Second check (Nested If): **Is the difference (Value1 - Value2) > Threshold?**  
   * If **True** → Message = `Value1 is significantly greater`.  
   * If **False** → Message = `Value1 is greater but margin is small`.  

---

##  **Step-by-Step Demo – Manual Trigger → If → Nested If → Results**

### Step 1: Start with a Manual Trigger

* Drag in a **Manual Trigger Node**.  
* This node is just a starting point so you can run the workflow by clicking **Execute Workflow**.  
* No configuration is needed here.

---

### Step 2: Add the First If Node (Primary Comparison)

* Drag in an **If Node**.  
* Connect: **Manual Trigger → If Node**.  
* Configure it like this:
  * **Value 1:** `={{20}}`  
  * **Operation:** `larger`  
  * **Value 2:** `={{5}}`  

➡ This checks if **20 > 5**.  

---

### Step 3: Handle the False Path (Value2 is greater or equal)

* From the **False output** of the If Node, add a **Set Node**.  
* Configure it like this:
  ```json
  {
    "message": "Value2 is greater or equal"
  }
  ```  

➡ If the condition fails, this message will be the result.

---

### Step 4: Add a Nested If Node (Margin Check)

* From the **True output** of the first If Node, add another **If Node**.  
* Rename it to **Nested If (Margin)**.  
* Configure it like this:
  * **Value 1:** `={{20 - 5}}`  
  * **Operation:** `larger`  
  * **Value 2:** `={{8}}`  

➡ This checks if the **difference (15) > 8**.  

---

### Step 5: Handle Nested If (True Path = High Margin)

* From the **True output** of the Nested If Node, add a **Set Node**.  
* Configure it like this:
  ```json
  {
    "message": "Value1 is significantly greater"
  }
  ```

---

### Step 6: Handle Nested If (False Path = Low Margin)

* From the **False output** of the Nested If Node, add a **Set Node**.  
* Configure it like this:
  ```json
  {
    "message": "Value1 is greater but margin is small"
  }
  ```

---

### Step 7: Run the Workflow

* Click **Execute Workflow**.  
* Try these cases:
  * **Case 1:** Value1 = 20, Value2 = 5 → True → Nested True → Message = `Value1 is significantly greater`.  
  * **Case 2:** Value1 = 10, Value2 = 5 → True → Nested False → Message = `Value1 is greater but margin is small`.  
  * **Case 3:** Value1 = 3, Value2 = 5 → False → Message = `Value2 is greater or equal`.  

---

##  **Key Takeaway for Students**

 **Manual Trigger** starts the workflow.  
 **If Node** makes the first decision.  
 **Nested If** refines the decision further.  
 **Different Set Nodes** provide clear outputs for each path.  

Together, this shows how to build **multi-level decisions** in n8n using nested If nodes.

---
