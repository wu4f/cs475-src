from langchain_google_genai import GoogleGenerativeAIEmbeddings
import math

embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query")
phrase1 = "This is a test document."
vec1 = embeddings.embed_query(phrase1)
phrase2 = "This is the test document."
vec2 = embeddings.embed_query(phrase2)
phrase3 = "Hello, how are you doing?"
vec3 = embeddings.embed_query(phrase3)

euclidean_distance = math.sqrt(sum((x - y) ** 2 for x, y in zip(vec1, vec2)))
print(f"Euclidean distance is: {euclidean_distance}")
euclidean_distance = math.sqrt(sum((x - y) ** 2 for x, y in zip(vec2, vec3)))
print(f"Euclidean distance is: {euclidean_distance}")
#print(f"{type(query_result)} {len(query_result)} {query_result[:5]}")
