from langchain_text_splitters import RecursiveCharacterTextSplitter
from documents import DOCUMENTS

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
)

all_chunks = []
for doc in DOCUMENTS:
    chunks = text_splitter.split_text(doc)
    all_chunks.extend(chunks)

print(f"원본 문서 수: {len(DOCUMENTS)}")
print(f"분할된 청크 수: {len(all_chunks)}")
print("\n처음 3개 청크:")
for i, chunk in enumerate(all_chunks[:3]):
    print(f"\n[청크 {i+1}] - {len(chunk)}")
    print(chunk)