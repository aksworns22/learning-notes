from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

load_dotenv()

gpt_o4_mini = init_chat_model(
    "openai:gpt-4o-mini",
    temperature=0.7,
    max_tokens=150
)

response_mini = gpt_o4_mini.invoke(
    [HumanMessage("안녕하세요? 반갑습니다")]
)

print(response_mini)

from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class CounterState(TypedDict):
    count: int


def increment(state: StateGraph) -> CounterState:
    print(f"현재 카운트: {state['count']}")
    new_count = state['count'] + 1
    print(f"새로운 카운트: {new_count}")
    return {"count": new_count}

graph = StateGraph(CounterState)
graph.add_node("increment", increment)
graph.add_edge(START, "increment")
graph.add_edge("increment", END)

app = graph.compile()
result = app.invoke({"count": 0})
print(f"최종 결과: {result}")
