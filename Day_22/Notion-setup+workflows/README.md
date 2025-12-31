# Connect a Notion Database to n8n (Internal Integration)

This guide shows **exactly** how to create a Notion database, make an **Internal integration**, give it access to your page, and then **connect it to n8n**. Every step includes a screenshot.

---

## What you’ll set up
- A Notion database page (table view).
- A Notion **Internal Integration** with a **Secret Key**.
- Page-level access granted to that integration.
- n8n credentials configured with that secret, so your workflows can read/write Notion data.

---

## Prerequisites
- A Notion account and a workspace you can manage.
- An n8n instance (Cloud or self‑hosted).

---

## Step‑by‑step

### 1) Open Notion and sign in
Go to **https://www.notion.so/** and sign in to your workspace.

> Link: https://www.notion.so/

### 2) Create a Database page (Table) in your **Private** section
In Notion’s left menu, go to **Private → “+” Add a page** and create a **Database** (Table) page.  
Use any columns you like (e.g., Name, Number, Description, Email).

![Create Database Page](images/Create-databse-page.png)
![Create Table](images/create-table.png)

### 3) Open **Connections → Develop or manage integrations**
In Notion, open **Settings & members → Connections → Develop or manage integrations**.

![Develop or manage integrations](images/manage-integrations.png)

### 4) Create a **New Integration**
Fill the form as shown:

- **Integration name:** Any name (e.g., *Botcampus page*)
- **Associated workspace:** Select your workspace
- **Type:** **Internal**
- **Logo:** Optional

Click **Save**.

![New Integration](images/new-integration.png)

### 5) Copy your **Internal Integration Secret**
In the integration **Configuration** tab, click **Show** to reveal the **Internal Integration Secret**. **Copy** it—this will be pasted into n8n credentials.

![Internal Integration Secret](images/secret-key.png)

### 6) Give the integration access to your Database page
- Go back to the Notion **homepage** and open your **Database page**.
- Click the **⋯** menu (top‑right) → **Connections**.
- Search and select your integration (e.g., *Botcampus page*), then **Confirm**.

![Add connection on page](images/page-connection-acces.png)
![Confirm connection](images/confirm-connection.png)

You should now see the page open with your content—this confirms you’re on the correct page.

![Page created](images/page-created.png)

### 7) (Optional) Share and copy the public link
If you need to share the page externally, click **Share** and **Copy link**.

### 8) Head over to **n8n** and add Notion credentials
- In n8n, search for **Notion** and open **Credentials**.
- Paste the **Internal Integration Secret** you copied in **Step 5**.
- Click **Test connection**.

![Configure Notion credentials in n8n](images/configure-to-n8n.png)

### 9) Verify the connection
You should see **Connection tested successfully**. Your Notion account is now connected to n8n.

---

## Notes & best practices
- **Permissions:** When you attach the integration to a page, it gets the abilities listed in the confirmation dialog (read, insert, update, comment).  
- **Granular access:** Only pages you explicitly connect will be accessible to the integration.
- **Database properties:** Keep column names tidy and choose proper property types (Text, Number, Email, etc.) to avoid mapping issues in n8n.

---

## Useful Notion references
- Notion: https://www.notion.so/
- Notion Developers – Integrations: https://www.notion.so/help/add-and-manage-integrations
- Notion API basics: https://developers.notion.com/

---

### You’re done!
You can now use Notion nodes in n8n to **query, create, and update** rows in your connected database.
