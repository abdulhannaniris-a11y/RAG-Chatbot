# 🤖 RAG Chatbot

An AI-powered Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF or TXT documents and ask questions based only on the uploaded content.

Built using **Streamlit**, **Groq LLM**, **Sentence Transformers**, and **FAISS Vector Database**.

---

## 🚀 Features

- 📄 Upload PDF and TXT documents
- 🧠 AI answers only from uploaded documents
- 🔍 Semantic search using embeddings
- ⚡ Fast retrieval with FAISS
- 🤖 Groq LLM for response generation
- 📚 Displays source pages used to answer
- 🔒 Secure API key management using Streamlit Secrets

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Groq API
- Sentence Transformers
- FAISS
- PyPDF
- NumPy

---

## 📂 Project Structure

```
RAG-Chatbot/
│
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
│
├── utils/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── vector_store.py
│   └── rag.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/abdulhannaniris-a11y/RAG-Chatbot.git
```

Go into the project

```bash
cd RAG-Chatbot
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup API Key

Create a file:

```
.streamlit/secrets.toml
```

Add your Groq API key:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

> Never commit this file to GitHub.

---

## ▶️ Run the App

```bash
streamlit run app.py
```

The app will open in your browser at:

```
http://localhost:8501
```

---

## 💡 How It Works

1. Upload one or more PDF/TXT documents.
2. Documents are split into smaller text chunks.
3. Sentence Transformers generate embeddings.
4. FAISS indexes the embeddings.
5. Relevant chunks are retrieved based on the user's question.
6. Retrieved context is sent to the Groq LLM.
7. The chatbot generates an answer using only the retrieved context.

---

## 📸 Demo

Upload a document and ask questions such as:

- Compare Honda Civic and Toyota Corolla.
- Which bike has the highest top speed?
- What is the fuel efficiency of the Honda City?

---

## 🔒 Security

- API keys are stored securely using Streamlit Secrets.
- Secrets are excluded from version control via `.gitignore`.

---

## 📈 Future Improvements

- Multi-document chat
- Chat history
- Conversation memory
- Citation highlighting
- Image support
- OCR for scanned PDFs
- Drag & Drop uploads
- Vector database persistence
- Multi-user support

---

## 👨‍💻 Author

**Abdul Hannan**

GitHub:
https://github.com/abdulhannaniris-a11y

LinkedIn:
(Add your LinkedIn profile here)

---

## ⭐ If you found this project useful

Please consider giving this repository a ⭐ on GitHub.
