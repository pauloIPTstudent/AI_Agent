from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# 1. Define o que o grafo "lembra"
class AgentState(TypedDict):
    messages: List[str] # Ou BaseMessage da LangChain

# 2. Define o nó do Orquestrador
def maestro_node(state: AgentState):
    # Aqui entrará a lógica da LLM futuramente
    last_msg = state['messages'][-1]
    return {"messages": [f"Maestro processou: {last_msg}"]}

# 3. Constrói o Grafo
workflow = StateGraph(AgentState)
workflow.add_node("maestro", maestro_node)
workflow.set_entry_point("maestro")
workflow.add_edge("maestro", END)

# Compila o grafo
maestro_app = workflow.compile()