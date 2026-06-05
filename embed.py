from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model loaded!")

sentence = """
This is a test sentence.
"""

embedding = model.encode(
    sentence
)

print(
    f"Embedding dimension: {len(embedding)}"
)

print(
    embedding[:10]
)