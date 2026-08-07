"""
text_splitter.py

Splits extracted documents into overlapping chunks
for embedding generation.
"""


def split_text(text, chunk_size=500, overlap=100):
    """
    Splits a single text into overlapping chunks.

    Args:
        text (str): Text to split
        chunk_size (int): Characters per chunk
        overlap (int): Overlap between chunks

    Returns:
        list: List of text chunks
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def create_chunks(documents, chunk_size=500, overlap=100):
    """
    Creates chunks from extracted documents while
    preserving metadata.

    Args:
        documents (list): Output from load_documents()

    Returns:
        tuple:
            document_chunks
            chunk_metadata
    """

    document_chunks = []
    chunk_metadata = []

    for document in documents:

        chunks = split_text(
            document["text"],
            chunk_size,
            overlap
        )

        for chunk_number, chunk in enumerate(chunks, start=1):

            document_chunks.append(chunk)

            chunk_metadata.append({
                "file_name": document["file_name"],
                "page": document["page"],
                "chunk": chunk_number
            })

    return document_chunks, chunk_metadata
