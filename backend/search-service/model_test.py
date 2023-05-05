from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
sentence1 = "This is a test sentence."
sentence2 = "This is another test sentence."
sentence3 = "Completely unrelated sentence."

embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)
embedding3 = model.encode(sentence3)

similarity12 = 1 - cosine(embedding1, embedding2)
similarity13 = 1 - cosine(embedding1, embedding3)

print(f"Similarity between sentence 1 and 2: {similarity12}")
print(f"Similarity between sentence 1 and 3: {similarity13}")