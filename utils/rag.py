"""
rag.py

Retrieval-Augmented Generation using
Groq + FAISS.
"""

from groq import Groq


class RAGChatbot:

    def __init__(self, api_key, vector_store, model_name="llama-3.3-70b-versatile"):

    self.client = Groq(api_key=api_key)

    print("===== GROQ DIAGNOSTIC =====")
    print("API KEY RECEIVED:", bool(api_key))
    print("MODEL REQUESTED:", model_name)

    try:
        models = self.client.models.list()

        print("AVAILABLE MODELS:")
        for model in models.data:
            print(model.id)

    except Exception as e:
        print("MODEL LIST ERROR:", repr(e))
        raise

    self.vector_store = vector_store
    self.model_name = model_name


    def ask(self, question, top_k=3):

        retrieved_chunks = self.vector_store.retrieve(
            question,
            top_k
        )

        context = "\n\n".join(
            [chunk["text"] for chunk in retrieved_chunks]
        )

        prompt = f"""
You are an AI assistant that answers ONLY from the provided context.

Rules:
1. Answer only using the context below.
2. If the answer is not available, reply exactly:
"I could not find this information in the uploaded documents."
3. Do not make up information.

Context:
{context}

Question:
{question}
"""

        response = self.client.chat.completions.create(

            model=self.model_name,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        answer = response.choices[0].message.content

        return answer, retrieved_chunks
