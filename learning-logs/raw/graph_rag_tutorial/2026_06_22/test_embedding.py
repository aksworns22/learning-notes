from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

text = "GraphRAG는 그래프와 RAG를 결합한 기술입니다."

vector = embeddings.embed_query(text)
print(f"임베딩 차원: {len(vector)}")
print(f"처음 5개 값: {vector[:5]}")