import numpy as np
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def cosine_similarity(vec1, vec2):
    """두 벡터의 코사인 유사도 계산"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

sentences = [
    "오늘 날씨가 정말 좋습니다.",
    "화창한 하늘이 아름답네요.",
    "파이썬 프로그래밍을 배웁니다.",
    "비가 많이 내립니다.",
]

vectors = embeddings.embed_documents(sentences)

print("기준:", sentences[0])
print('-' * 50)

for i in range(1, len(sentences)):
    similarity = cosine_similarity(vectors[0], vectors[i])
    print(f"{sentences[i]}")
    print(f"  → 유사도: {similarity:.4f}")
    print()
