import streamlit as st

from utils.document_loader import load_documents
from utils.text_splitter import create_chunks
from utils.vector_store import VectorStore
from utils.rag import RAGChatbot


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG Chatbot")
st.caption("Upload PDF or TXT files and chat with them using AI.")


# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "rag" not in st.session_state:
    st.session_state.rag = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "knowledge_ready" not in st.session_state:
    st.session_state.knowledge_ready = False


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    top_k = st.slider(
        "Retrieved Chunks",
        min_value=1,
        max_value=10,
        value=3
    )

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    if st.button("🔄 Reset Knowledge Base"):

        st.session_state.vector_store = None
        st.session_state.rag = None
        st.session_state.knowledge_ready = False
        st.session_state.messages = []

        st.success("Knowledge Base Reset!")

        st.rerun()
      # ---------------------------------------------------
# Build Knowledge Base
# ---------------------------------------------------

if uploaded_files and not st.session_state.knowledge_ready:

    with st.spinner("📄 Reading documents..."):

        documents = load_documents(uploaded_files)

    if len(documents) == 0:

        st.error("No readable text found in the uploaded files.")

        st.stop()

    with st.spinner("✂️ Creating text chunks..."):

        document_chunks, chunk_metadata = create_chunks(documents)

    with st.spinner("🧠 Generating embeddings..."):

        vector_store = VectorStore()

        vector_store.build_index(
            document_chunks,
            chunk_metadata
        )

    try:

        rag = RAGChatbot(

            api_key=st.secrets["GROQ_API_KEY"],

            vector_store=vector_store
        )

        st.session_state.vector_store = vector_store

        st.session_state.rag = rag

        st.session_state.knowledge_ready = True

        st.success("✅ Knowledge Base Ready!")

    except Exception as error:

        st.error(f"Failed to initialize Groq: {error}")

        st.stop()
# ---------------------------------------------------
# Chat Interface
# ---------------------------------------------------

# Display previous chat messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and "sources" in message:

            with st.expander("📚 Sources"):

                shown = set()

                for source in message["sources"]:

                    metadata = source["metadata"]

                    key = (
                        metadata["file_name"],
                        metadata["page"]
                    )

                    if key not in shown:

                        shown.add(key)

                        st.write(
                            f"📄 **{metadata['file_name']}** "
                            f"(Page {metadata['page']})"
                        )


# Chat input
question = st.chat_input("Ask something about your uploaded documents...")

if question:

    # Check if knowledge base exists
    if not st.session_state.knowledge_ready:

        st.warning("⚠️ Please upload at least one PDF or TXT file first.")

        st.stop()

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer, sources = st.session_state.rag.ask(
                question,
                top_k
            )

            st.markdown(answer)

            with st.expander("📚 Sources"):

                shown = set()

                for source in sources:

                    metadata = source["metadata"]

                    key = (
                        metadata["file_name"],
                        metadata["page"]
                    )

                    if key not in shown:

                        shown.add(key)

                        st.write(
                            f"📄 **{metadata['file_name']}** "
                            f"(Page {metadata['page']})"
                        )

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources
        }
    )
