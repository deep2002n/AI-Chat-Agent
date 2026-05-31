#!/usr/bin/env python
# coding: utf-8

# In[98]:


def set_env():
    import os
    os.chdir("c:/in_genai")
    import getpass
    # Set the environment variable
    #API_KEY1 = input("Give the value of GEMINI API KEY ")
    with open("apikey2.txt", "r", encoding="utf-8") as f:
       API_KEY1 = f.read().strip()
    os.environ["GEMINI_API_KEY"] = API_KEY1
    return API_KEY1



# In[10]:


def chroma_processing():
   import chromadb 
   client_ch = chromadb.Client()
   collection = client_ch.get_or_create_collection(name="refund_policy")
   #collection = client.create_collection(name="refund_policy")
   f = open("c:/in_genai/refund_policy.txt","r",encoding="utf-8")

   # Step 2: Read the contents
   policy_text1 = f.read()

   # Step 3: Close the file
   f.close()

   # Step 4: Display contents
   #print(policy_text1)

   collection.upsert(documents=[policy_text1], ids=["refund_policy"])
   return policy_text1 


# In[99]:


def create_prompt(question1,policy_text2):
    #question1 = "Can I return a laptop after 10 days by 'custid -4444'?"

    result1 = {
    "customer id" : "id from question text only numerical part",
    "category": "Complaint",
    "sentiment": "Negative",
    "priority": "HIGH",
    "Desc" : "Polite response in max 150 char incuding spaces",
    "next action" : "callback or refund or cancellation"
    }

    prompt1 = f"""
    Role : You are a customer support representative.
    Always respond politely and professionally.

    Use only the policy below. 
    Policy: {policy_text2}

    Question:
    {question1}

    Result format  {result1}

    Return ONLY valid JSON.

    Rules:
    1. Use double quotes for all keys and values.
    2. Do not use single quotes.
    3. Do not wrap in ```json code blocks.
    4. Return one JSON object only.
    """

    return prompt1


# In[27]:


def response(prompt1, API_KEY1):
    from google import genai
    from google.genai import types
    import json
    client = genai.Client(api_key=API_KEY1)
    '''response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt1,
    config={"response_mime_type": "application/json"})
    print(response.text)
    result1=json.loads(response.text)'''
    result1 = {
    "customer id" : 100,
    "category": "Complaint",
    "sentiment": "Negative",
    "priority": "HIGH",
    "Desc" : "testing without gemini",
    "next action" : "callback"
    }
    
    return result1



# In[100]:


def gen_ticket(result1):
   import sqlite3 
   conn1 = sqlite3.connect("company2.db")
   cursor1 = conn1.cursor()
   cursor1.execute("""
   CREATE TABLE IF NOT EXISTS ticket_table (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    category TEXT,
    sentiment TEXT,
    priority TEXT,
    description TEXT,
    next_action TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
   )
   """)
   #if result1['customer id'] in (""," ", '',' ', None):
   #   result1['customer id'] = 0
   #else:
   #   result1['customer id'] = int(result1['customer id'])
   result1['customer id']=1000
   cursor1.execute("""
   INSERT INTO ticket_table (
    customer_id,
    category,
    sentiment,
    priority,
    description,
    next_action
     )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
   (
    result1["customer id"],
    result1["category"],
    result1["sentiment"],
    result1["priority"],
    result1["Desc"],
    result1["next action"]
   ))

   conn1.commit()
   ticket_id1 = cursor1.lastrowid
   #print("Generated Ticket ID:", ticket_id1)
   conn1.close()
   return ticket_id1  



# In[104]:


def process_email(ticket_id1, result1):
    from email_util import send_email
    subject=f'Ticket id - {ticket_id1} generated for {result1["category"]}'
    body=f'{result1}  {result1["next action"]}_table updated, check workflow_log table for complete info'
    to="info@medhavart.com"
    send_email(to,body,subject)
    return subject, body


# In[102]:


def process_question(question1):
    API_KEY1=set_env()
    policy_text2=chroma_processing()
    prompt1=create_prompt(question1, policy_text2)
    result1=response(prompt1, API_KEY1)
    ticket_id1=gen_ticket(result1)
    subject1, email_body1=process_email(ticket_id1,result1)
    return result1, subject1, email_body1



# In[ ]:


#result1,subject1,email_body1=process_question("can I return in 53 days custid ")

