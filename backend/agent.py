from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
import os

GROQ_API_KEY=os.getenv("GROQ_API_KEY")


class CodeCoachState(TypedDict):
    code: str
    language: str
    vulnerabilities: List[dict]
    refactored_code: str
    docs: str

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)


# 3. Define the Nodes (Async)
async def security_auditor(state: CodeCoachState):
    """Focuses only on security flaws."""
    prompt = f"Act as a Security Engineer. Find bugs/vulnerabilities in this {state['language']} code:\n{state['code']}\nReturn a list of findings with line numbers."
    response = await llm.ainvoke(prompt)
    return {"vulnerabilities": [{"issue": response.content}]}


async def code_architect(state: CodeCoachState):
    """Focuses on refactoring and clean code (SOLID principles)."""
    prompt = f"Act as a Senior Developer. Refactor this code for readability and performance. Return ONLY the code:\n{state['code']}"
    response = await llm.ainvoke(prompt)
    return {"refactored_code": response.content}


async def doc_specialist(state: CodeCoachState):
    """Generates documentation based on the refactored code."""
    prompt = f"Write a professional README and Docstrings for the following code:\n{state['refactored_code']}"
    response = await llm.ainvoke(prompt)
    return {"docs": response.content}

workflow = StateGraph(CodeCoachState)

workflow.add_node("auditor", security_auditor)
workflow.add_node("architect", code_architect)
workflow.add_node("docs", doc_specialist)

workflow.add_edge(START, "auditor")
workflow.add_edge("auditor", "architect")
workflow.add_edge("architect", "docs")
workflow.add_edge("docs", END)

app_graph = workflow.compile()
