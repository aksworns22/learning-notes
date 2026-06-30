from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from documents import DOCUMENTS

load_dotenv()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=30
)

chunks = []
for doc in DOCUMENTS:
    chunks.extend(text_splitter.split_text(doc))

print(f"총 {len(chunks)}개 청크 생성")

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = InMemoryVectorStore(embeddings)
vector_store.add_texts(chunks)

print("벡터 저장소 구축 완료!")

retriever = vector_store.as_retriever(search_kwargs={'k': 3})

template = """다음 컨텍스트를 바탕으로 질문에 답해주세요.
컨텍스트에 없는 내용은 "해당 정보를 찾을 수 없습니다"라고 답하세요.

컨텍스트:
{context}

질문: {question}

답변:"""

prompt = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = {'context': retriever | format_docs, 'question': RunnablePassthrough()} | prompt | llm | StrOutputParser()

questions = [
    "세종대왕이 발명한 것들은 무엇인가요?",
    "정조는 어떤 정책을 실시했나요?",
    "이순신 장군의 명량해전에 대해 알려주세요.",
]

print("=" * 60)
print("RAG 시스템 테스트")
print("=" * 60)

for q in questions:
    print(f"\n질문: {q}")
    answer = rag_chain.invoke(q)
    print(f"답변: {answer}")
    print("-" * 60)

difficult_questions = [
    # 관계 추론 필요
    "세종대왕과 집현전의 관계는 무엇인가요?",

    # 다단계 추론 필요
    "세종대왕이 설치한 기관에서 누가 활동했나요?",

    # 비교 질문
    "세종대왕과 정조의 공통점은 무엇인가요?",

    # 시간순 나열
    "조선의 왕들을 시대순으로 나열해주세요.",
]

print("=" * 60)
print("전통 RAG의 한계 테스트")
print("=" * 60)

for q in difficult_questions:
    print(f"\n질문: {q}")

    # 검색된 문서 확인
    docs = retriever.invoke(q)
    print("\n[검색된 문서]")
    for i, doc in enumerate(docs, 1):
        print(f"  {i}. {doc.page_content[:50]}...")

    # 답변 생성
    answer = rag_chain.invoke(q)
    print(f"\n[답변]\n{answer}")
    print("-" * 60)