from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm: ChatOpenAI = ChatOpenAI(model="gpt-4o-mini", temperature=0)

response = llm.invoke("안녕하세요! 한 문장으로 자기소개 해주세요.")
print(f"GPT 응답: {response.content}")