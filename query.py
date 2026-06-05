
import chromadb
from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path="./vectordb"
)

collection = client.get_or_create_collection(
    name="persona"
)

print("Ready!")

while True:

    question = input(
        "\nQuestion: "
    )

    if question.lower() == "exit":
        break

    embedding = model.encode(
        question
    )

    results = collection.query(
        query_embeddings=[
            embedding.tolist()
        ],
        n_results=4
    )

    print("\nRESULTS:\n")

    for i, doc in enumerate(
        results["documents"][0]
    ):
        print(
            f"\nChunk {i+1}\n"
        )
        print(doc[:500])

