import os
import PyPDF2
from sentence_transformers import SentenceTransformer
import chromadb
from django.conf import settings
from asgiref.sync import sync_to_async

# Sentence embedding model initialization
EMBEDDING_MODEL = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', cache_folder='/data/base_models')

# ChromaDB client initialization and collection creation
CHROMA_CLIENT = chromadb.Client()
COLLECTION = CHROMA_CLIENT.create_collection(name="rag_llama2")

CHUNK_SIZE = 1500
OVERLAP_SIZE = 150


def chunking(path):
    """
    Chunk the PDF document.

    Args:
        path (str): Path to the PDF file.

    Returns:
        list: List of overlapping chunks of text.
    """
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        reader = PyPDF2.PdfReader(file_path)
        pages = [page.extract_text() for page in reader.pages]
        document = '\n'.join(pages)
        return get_overlapped_chunks(document, CHUNK_SIZE, OVERLAP_SIZE)
    except Exception as e:
        print(f"Error in chunking: {e}")
        return []


def get_overlapped_chunks(textin, chunksize, overlapsize):
    """
    Generate overlapping chunks of text.

    Args:
        textin (str): Input text.
        chunksize (int): Size of each chunk.
        overlapsize (int): Size of overlap between chunks.

    Returns:
        list: List of overlapping text chunks.
    """
    return [textin[a:a+chunksize] for a in range(0, len(textin), chunksize-overlapsize)]


@sync_to_async
def context(path, query):
    """
    Get context based on a PDF file and a query.

    Args:
        path (str): Path to the PDF file.
        query (str): Query string.

    Returns:
        str: Relevant context based on the query.
    """
    try:
        chunks = chunking(path)
        if not chunks:
            return ""

        calculate_embeddings(chunks, query)
        retrieved_results = retrieve_vector_db(query)

        context = '\n\n'.join(retrieved_results[0])
        doc_ids = COLLECTION.get()["ids"]
        COLLECTION.delete(ids=doc_ids)

        return context
    except Exception as e:
        print(f"Error in context: {e}")
        return ""


def calculate_embeddings(chunks, query):
    """
    Generate embeddings for text chunks.

    Args:
        chunks (list): List of text chunks.
        query (str): Query string.

    Returns:
        None
    """
    chunk_embeddings = EMBEDDING_MODEL.encode(chunks)
    COLLECTION.add(
        embeddings=chunk_embeddings,
        documents=chunks,
        ids=[str(i) for i in range(len(chunks))]
    )


def retrieve_vector_db(query, n_results=3):
    """
    Retrieve relevant documents based on the query.

    Args:
        query (str): Query string.
        n_results (int): Number of results to retrieve.

    Returns:
        list: Relevant documents.
    """
    results = COLLECTION.query(
        query_embeddings=EMBEDDING_MODEL.encode(query).tolist(),
        n_results=n_results
    )
    return results['documents']
