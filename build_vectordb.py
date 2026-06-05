from ingest import (
    load_resume,
    load_readmes,
    load_commits,
    chunk_text
)

from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

all_chunks = []


resume = load_resume(
    "data/Riyashah1.pdf"
)

for chunk in chunk_text(resume):
    all_chunks.append(chunk)


readmes = load_readmes(
    "data/github"
)

for doc in readmes:

    for chunk in chunk_text(
        doc["text"]
    ):

        all_chunks.append(chunk)


for repo in Path(
    "data/github"
).iterdir():

    if repo.is_dir():

        commits = load_commits(
            str(repo)
        )

        for commit in commits:

            text = f"""
Repository: {repo.name}

Author: {commit['author']}

Date: {commit['date']}

Commit Message:
{commit['message']}
"""

            all_chunks.append(
                text
            )

print("=" * 50)
print(f"Total chunks: {len(all_chunks)}")
print("=" * 50)

print("Generating embeddings...")

embeddings = model.encode(
    all_chunks
)

client = chromadb.PersistentClient(
    path="./vectordb"
)

collection = client.get_or_create_collection(
    name="persona"
)


try:
    existing = collection.get()
    if existing["ids"]:
        collection.delete(
            ids=existing["ids"]
        )
except:
    pass

print("Saving to ChromaDB...")

for i, chunk in enumerate(all_chunks):

    collection.add(
        ids=[str(i)],
        documents=[chunk],
        embeddings=[
            embeddings[i].tolist()
        ]
    )

print("Done!")