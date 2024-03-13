# IfPdf.py

import os
import PyPDF2
from sentence_transformers import SentenceTransformer
import chromadb
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
import torch


def context(path, query):
    # Chunk the PDF document and obtain embeddings for each chunk
    chunks = Chunking(path)
    embeddings = Embeddings(chunks, query)
    
    # Retrieve relevant results from the vector database
    retrieved_results = retrieve_vector_db(query)
    
    # Concatenate retrieved results for context
    context = '\n\n'.join(retrieved_results[0])
    print(context)
    return context


def Chunking(path):
    # Use os.path.join to concatenate path and filename
    file_path = os.path.join(path)
    
    # Create a PDF reader object
    reader = PyPDF2.PdfReader(file_path)

    # Extract text from each page and concatenate
    pages = [page.extract_text() for page in reader.pages]
    document = '\n'.join(pages)

    # Split the document into overlapping chunks
    chunks = get_overlapped_chunks(document, 1000, 100)

    return chunks


def get_overlapped_chunks(textin, chunksize, overlapsize):  
    # Generate overlapping chunks of text
    return [textin[a:a+chunksize] for a in range(0, len(textin), chunksize-overlapsize)]


# Sentence embedding model initialization
embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', cache_folder='/data/base_models')

# ChromaDB client initialization and collection creation
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="rag_llama2")


def Embeddings(chunks, query):
    # Generate embeddings for text chunks using the Sentence Transformer model
    chunk_embeddings = embedding_model.encode(chunks)

    # Add the chunk embeddings, documents, and IDs to the ChromaDB collection
    collection.add(
        embeddings=chunk_embeddings,
        documents=chunks,
        ids=[str(i) for i in range(len(chunks))]
    )


# Retrieval of relevant documents based on the query
def retrieve_vector_db(query, n_results=3):
    results = collection.query(
        query_embeddings=embedding_model.encode(query).tolist(),
        n_results=n_results
    )
    return results['documents']
