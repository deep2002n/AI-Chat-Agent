import streamlit as st

from customer import process_question


st.title("Customer Support Assistant26")

subject1=None

question1 = st.text_area("Enter Customer Question")

if st.button("Submit"):
    result1, subject1, email_body1 = process_question(question1)
    st.write(result1["Desc"])
            
with st.expander("Show Details"):
    
   if subject1:
       # A completely flat variable with no placeholders
       style = "<span style='color: green; font-size: 15px; font-weight: bold;'>"
       st.html(f"{style}Step 1 - </span>AI response created based on the customer question")
       st.html(f"{style}Step 2 - </span>{subject1}")
       st.html(f"{style}Step 3 - </span>email sent info@medhavart support team, email body - {email_body1}")
       st.html(f"{style}Step 4 - </span>{result1['next action']}_table updated by the database trigger")
       st.html(f"{style}Step 5 - </span>workflow_log table updated by the database trigger")



       
       
       