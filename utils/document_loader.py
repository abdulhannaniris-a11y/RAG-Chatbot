"""
document_loader.py

Handles loading and extracting text from PDF and TXT files.
"""

from pypdf import PdfReader


def load_documents(uploaded_files):
    """
    Reads uploaded PDF/TXT files and extracts text.

    Returns:
        documents (list): List of dictionaries containing:
            - file_name
            - page
            - text
    """

    documents = []

    for uploaded_file in uploaded_files:

        file_name = uploaded_file.name

        # -------------------------------
        # PDF Files
        # -------------------------------
        if file_name.lower().endswith(".pdf"):

            try:
                reader = PdfReader(uploaded_file)

                for page_number, page in enumerate(reader.pages, start=1):

                    text = page.extract_text()

                    if text and text.strip():

                        documents.append({
                            "file_name": file_name,
                            "page": page_number,
                            "text": text.strip()
                        })

            except Exception as error:

                print(f"Error reading PDF '{file_name}': {error}")

        # -------------------------------
        # TXT Files
        # -------------------------------
        elif file_name.lower().endswith(".txt"):

            try:

                text = uploaded_file.read().decode("utf-8")

                if text.strip():

                    documents.append({
                        "file_name": file_name,
                        "page": 1,
                        "text": text.strip()
                    })

            except Exception as error:

                print(f"Error reading TXT '{file_name}': {error}")

    return documents
