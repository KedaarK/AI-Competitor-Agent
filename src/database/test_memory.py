# test_memory.py
from src.database.memory import query_memory

# Search for "Fitness" across all stored competitors
results = query_memory("How do athletes train?")

print("Memory found these relevant posts:")

if results:
    for doc_list in results:
        for doc in doc_list:
            print(f"- {doc}")
else:
    print("No results found.")