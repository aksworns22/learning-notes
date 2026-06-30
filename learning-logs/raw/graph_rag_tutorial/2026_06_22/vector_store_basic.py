from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = InMemoryVectorStore(embeddings)

documents = [
    "세종대왕은 한글을 창제한 조선의 왕입니다.",
    "이순신 장군은 임진왜란에서 왜군을 물리쳤습니다.",
    "파이썬은 배우기 쉬운 프로그래밍 언어입니다.",
    "서울은 대한민국의 수도입니다.",
    "김치는 한국의 전통 발효 음식입니다.",
    "훈민정음은 1443년에 창제되었습니다.",
]

vector_store.add_texts(documents)
print(f"{len(documents)}개 문서 추가 완료")

query = "Who makes Korean Language"
results = vector_store.similarity_search(query, k=3)

print(f"\n질문: {query}\n")
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.page_content}")
