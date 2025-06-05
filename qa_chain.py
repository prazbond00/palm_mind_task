from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI


def create_qa_chain(vectorstore):
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, retriever=vectorstore.as_retriever())
    return qa_chain
