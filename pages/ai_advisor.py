import os
import shutil
import streamlit as st
from dotenv import load_dotenv
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint

# ✅ Load environment variables FIRST
load_dotenv()
sec_key = os.getenv("HF_TOKEN")

# ✅ Define the LLM model with Hugging Face Endpoint
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_length=128,
    temperature=0.7,
    huggingfacehub_api_token=sec_key
)

# ✅ Use a better free embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# ✅ Define the page rendering function
def show_page():
    # Streamlit UI Setup
    st.title("FyPy: An AI-Powered Equity Analysis Tool")
    st.caption("Your AI Stock Research Chatbot - FyPy Advisor")

    # Sidebar Configuration
    with st.sidebar:
        st.header("Configuration")
        st.divider()
        st.markdown('### Capabilities')
        st.markdown("""
             - 📊 Stock Research  
             - 📰 Article Processing  
             - 🔍 Financial Insights  
         """)
        st.divider()

    # Managing Session State
    if "message_log" not in st.session_state:
        st.session_state.message_log = [{"role": "ai", "content": "Hi! I'm FyPy Advisor. How can I assist with stock research?"}]

    # Sidebar for URL Input
    st.sidebar.title("Stock Article URLs")
    file_path = "vectorIndex_mistral"
    urls = [st.sidebar.text_input(f"URL {i+1}") for i in range(3)]
    process_url_clicked = st.sidebar.button("Process URLs")

    if process_url_clicked:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)  # ✅ Remove directory
            else:
                os.remove(file_path)
        loader = UnstructuredURLLoader(urls=[url for url in urls if url])
        st.session_state.message_log.append({"role": "ai", "content": "Processing URLs..."})

        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ".", ","],
            chunk_size=300,
            chunk_overlap=20
        )
        docs = text_splitter.split_documents(data)

        # ✅ Save embeddings using FAISS
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local(file_path)

        st.session_state.message_log.append({"role": "ai", "content": "URLs processed and stored successfully!"})
        st.rerun()

    # Initiate the Chat Container
    chat_container = st.container()

    # Display Chat Messages
    with chat_container:
        for message in st.session_state.message_log:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Function to Generate AI Response
    def generate_ai_response(query):
        if os.path.exists(file_path):
            # ✅ Load FAISS vector store
            vectorstore = FAISS.load_local(file_path, embeddings, allow_dangerous_deserialization=True)
            
            # ✅ Use the correct LLM instance
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())

            result = chain({"question": query}, return_only_outputs=True)

            response = result["answer"]
            sources = result.get("sources", "")
            if sources:
                response += f"\n\n*Sources:*\n" + "\n".join(sources.split("\n"))
            return response
        else:
            return "No stock data available. Please process URLs first."

    # User Input
    user_query = st.chat_input("Type your stock-related questions...")

    if user_query:
        st.session_state.message_log.append({"role": "user", "content": user_query})
        with st.spinner("..Processing"):
            ai_response = generate_ai_response(user_query)
        st.session_state.message_log.append({"role": "ai", "content": ai_response})
        st.rerun()