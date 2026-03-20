# src/database/memory.py
import chromadb
from chromadb.utils import embedding_functions
import os
from typing import List
from chromadb.api.types import Metadata

# 1. Setup Local Storage Path
CHROMA_DATA_PATH = "data/chroma_db"
os.makedirs(CHROMA_DATA_PATH, exist_ok=True)

# 2. Setup the Embedding Function (HuggingFace Local)
default_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# 3. Initialize Chroma Client
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

def get_collection():
    """
    CRITICAL FIX: This function ensures that if the collection 
    was deleted by reset_memory(), it is recreated immediately.
    """
    return client.get_or_create_collection(
        name="competitor_posts", 
        embedding_function=default_ef # type: ignore
    )

def store_posts(competitor, posts_list):
    """Saves scraped posts into the local vector database."""
    if not posts_list:
        return

    # Use the helper function to get a valid collection handle
    current_collection = get_collection()

    ids = [f"{competitor}_{i}_{os.urandom(4).hex()}" for i in range(len(posts_list))]
    metadatas: List[Metadata] = [
        {"competitor": str(competitor)} for _ in posts_list
    ]

    current_collection.add(
        documents=posts_list,
        ids=ids,
        metadatas=metadatas
    )
    print(f"--- Stored {len(posts_list)} posts in Memory for {competitor} ---")

def query_memory(competitor_name, n_results=5):
    """
    STRICT FILTERING: This ensures the Agent only gets data 
    belonging to the specific competitor.
    """
    current_collection = get_collection()
    
    results = current_collection.query(
        query_texts=[f"Latest posts for {competitor_name}"],
        where={"competitor": str(competitor_name)}, 
        n_results=n_results
    )
    
    # SAFETY CHECK: If documents is None or empty, return an empty list
    docs = results.get('documents')
    
    if docs is None:
        print(f"--- Warning: No memory found for {competitor_name} ---")
        return []

    # Flatten the list: Chroma returns [[doc1, doc2]]
    # We use 'if sublist' to ensure we don't iterate over None
    return [doc for sublist in docs if sublist is not None for doc in sublist]

def reset_memory():
    """Deletes the current collection safely."""
    try:
        client.delete_collection(name="competitor_posts")
        print("--- Memory Reset: Old data cleared ---")
    except Exception as e:
        # Silent pass if collection didn't exist
        pass