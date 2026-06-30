import numpy as np
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

documents = [
    "세종대왕은 한글을 창제한 조선의 왕입니다.",
    "이순신 장군은 임진왜란에서 왜군을 물리쳤습니다.",
    "파이썬은 배우기 쉬운 프로그래밍 언어입니다.",
    "서울은 대한민국의 수도입니다.",
    "김치는 한국의 전통 발효 음식입니다.",
    "훈민정음은 1443년에 창제되었습니다.",
]

doc_vectors = embeddings.embed_documents(documents)


def search(query: str, top_k: int = 3) -> list:
    """질문과 가장 비슷한 문서 top_k개 반환"""
    query_vector = embeddings.embed_query(query)

    similarities = []
    for i, doc_vec in enumerate(doc_vectors):
        sim = cosine_similarity(query_vector, doc_vec)
        similarities.append((i, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)

    results = []
    for idx, sim in similarities[:top_k]:
        results.append({
            "document": documents[idx],
            "similarity": sim,
        })
    return results


query = "한글을 만든 왕은 누구인가요?"
print(f"질문: {query}", end="\n\n")

results = search(query, top_k=3)
for i, result in enumerate(results, 1):
    print(f"{i}. [{result['similarity']:.4f}] {result['document']}")
