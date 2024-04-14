import os
import PyPDF2
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize Sentence Transformer model
embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', cache_folder='/data/base_models')

# Initialize ChromaDB client
chroma_client = chromadb.Client()

def context(path, query):
    # Extract the filename without extension from the path
    filename = os.path.basename(path)
    collection_name = clean_collection_name(filename)

    # Create or get a unique collection name
    collection = get_unique_collection(collection_name)

    chunks = chunking(path)
    embeddings = embed_chunks(chunks, collection)
    retrieved_results = retrieve_vector_db(query, collection)
    context_text = '\n\n'.join(retrieved_results)
    return context_text


def clean_collection_name(name):
    # Replace invalid characters with underscores
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-')
    cleaned_name = ''.join(c if c in valid_chars else '_' for c in name)

    # Ensure the name starts and ends with an alphanumeric character
    if not cleaned_name[0].isalnum():
        cleaned_name = '_' + cleaned_name
    if not cleaned_name[-1].isalnum():
        cleaned_name = cleaned_name + '_'

    return cleaned_name


def get_unique_collection(name):
    existing_collections = chroma_client.list_collections()
    unique_name = name
    index = 1

    # Append index to name if it already exists
    while unique_name in existing_collections:
        unique_name = f"{name}_{index}"
        index += 1

    # Create a new collection with the unique name
    collection = chroma_client.create_collection(name=unique_name)
    return collection


def chunking(path):
    file_path = os.path.join(path)
    reader = PyPDF2.PdfReader(file_path)
    pages_text = [page.extract_text() for page in reader.pages]
    document_text = '\n'.join(pages_text)
    chunks = get_overlapped_chunks(document_text, chunk_size=300, overlap_size=50)
    return chunks


def get_overlapped_chunks(text, chunk_size, overlap_size):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - overlap_size)]
    return chunks


def embed_chunks(chunks, collection):
    chunk_embeddings = embedding_model.encode(chunks)
    # Store embeddings in ChromaDB
    for i, chunk in enumerate(chunks):
        collection.add(
            embeddings=chunk_embeddings[i],
            documents=chunk,
            ids=str(i)
        )


def retrieve_vector_db(query, collection):
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=3)
    return results['documents']

