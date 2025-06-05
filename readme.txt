#  AI Chatbot with Appointment & Call Form Integration

This is a console-based AI assistant powered by LangChain and OpenAI GPT-4. The assistant can:

- Answer questions from uploaded documents (PDF or TXT)
- Collect call-back details via a conversational form
- Book appointments using natural language dates
- Log conversations, call forms, and bookings


## Project Structure
app.py # Main app logic
├── qa_chain.py # Q/A chain creation logic
├── document_handler.py # Document loading & vector store creation
├── form_tools.py # Pydantic forms for call and booking
├── utils/
│ ├── date_parser.py # Parses natural date strings (e.g. "next Friday")
│ └── validators.py # Email and phone validators
├── conversation_logs/ # Stores chat logs in JSON format
├── .env # Stores API keys securely
├── requirements.txt # Python dependencies


##  Setup Instructions

### 1. Clone the repository

```bash
git clone 
cd chatbot_project

python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt

python app.py

Example Commands:
"call me later" — launches the call form
"I'd like to book an appointment for next Monday" — triggers the booking tool
"What is in this document?" — answers questions from your uploaded docs
"exit" — ends the session and saves the chat log
 

