This project is meant to chat with customers, at backend google gemini AI is active and is geting info from company policy doc

Features

Customers can as question.
AI will answer based on company policy which is already fed to AI
Based on category, sentiment and others, ticket will be generated in ticket database along with "next action" as callback,refund,cancellation
Email is sent to support with details and ticket number
Based on next action, related table (callback, refund, cancellation) is updated by database trigger.
Graph is plotted for sentiment 
The ticket data is uploaded to clound for furthur BI analysis. 
