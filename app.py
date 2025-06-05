import os
import json
from datetime import datetime
from dotenv import load_dotenv

from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from document_handler import load_documents, create_vector_store
from qa_chain import create_qa_chain
from form_tools import collect_call_form, collect_booking_form

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found. Please set it in your .env file.")

# Logs
conversation_log = []
call_logs = []
booking_logs = []


def save_conversation_log():
    log_dir = os.path.join(os.getcwd(), "conversation_logs")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_log_{timestamp}.json"
    data = {
        "conversation": conversation_log,
        "call_forms": call_logs,
        "appointments": booking_logs
    }
    with open(os.path.join(log_dir, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Conversation saved to: conversation_logs/{filename}")


def main():
    file_paths = input("Enter document file paths (comma separated): ")
    paths_list = [p.strip().strip("'\"")
                  for p in file_paths.split(",") if p.strip()]
    if not paths_list:
        print("No files entered. Exiting.")
        return

    print(f"📚 Loading documents from: {paths_list}")
    docs = load_documents(paths_list)

    # Initialize embeddings and vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = create_vector_store(docs, embeddings)

    # Create QA chain and memory
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history")
    qa_chain = create_qa_chain(vectorstore)

    # Define tools
    tools = [
        Tool(
            name="CallForm",
            func=lambda q: call_logs.append(
                collect_call_form()) or "✅ Call form submitted.",
            description="Collect user contact info."
        ),
        Tool(
            name="BookAppointment",
            func=lambda q: booking_logs.append(
                collect_booking_form()) or "📅 Appointment booked.",
            description="Schedule an appointment."
        ),
        Tool(
            name="DocQA",
            func=lambda q: qa_chain.invoke({"query": q})["result"],
            description="Answer questions based on the uploaded documents."
        ),
    ]

    # Initialize agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=memory,
        verbose=True
    )

    print("🤖 Chatbot is ready! Type 'call me', 'book appointment', or ask questions. Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit", "i am done"):
            print("Goodbye!")
            save_conversation_log()
            break

        conversation_log.append({"role": "user", "content": user_input})

        try:
            response = agent.run(user_input)
        except Exception as e:
            response = f"⚠️ Error: {e}"

        conversation_log.append({"role": "bot", "content": response})
        print(f"Bot: {response}")


if __name__ == "__main__":
    main()
