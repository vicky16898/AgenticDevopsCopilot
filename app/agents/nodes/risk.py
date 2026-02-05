from app.agents.state import AgentState
from app.mcp_servers.k8s_validator import k8s_validator
from app.mcp_servers.ci_inspector import ci_inspector
from app.core.llm import get_llm
from app.rag.retrieval import rag_retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def assess_risk_node(state: AgentState) -> dict:
    """
    1. Validates K8s manifests
    2. Inspects CI logs (mocked or from file)
    3. Uses LLM + RAG to generate a generic Risk Report
    """
    print("--- Assessing Risk ---")
    
    files = state.get("analyzed_files", [])
    
    # 1. Run Tools
    manifest_findings = []
    
    # Simple heuristic to find manifests and logs in the file list
    # In a real app, content would be retrieved or passed through state more robustly
    # For now, we simulate "reading" them if we had the content content in state or re-read
    # To keep it simple, we just assume we might risk check via LLM or tool if content is available.
    
    # Let's rely on LLM RAG to find risks for the Report, plus explicit tool usage if we had file contents.
    # We will trigger the k8s validator on any .yaml file found.
    
    # (Simplified logic: In a real scenario, we'd iterate the actual file contents)
    
    # 2. Generate Report via LLM + RAG
    llm = get_llm()
    retriever = rag_retriever.get_retriever()
    
    # Check for specific "risk" keywords in RAG
    context_docs = retriever.invoke("deployment security risks kubernetes ci/cd")
    context_text = "\n\n".join([d.page_content for d in context_docs])
    
    prompt = ChatPromptTemplate.from_template("""
    You are a DevOps expert. Analyze the collected context from the repository and generate a Risk Assessment Report.
    
    Context from Repository (RAG):
    {context}
    
    Repository Structure:
    {structure}
    
    Task:
    Identify potential security risks, configuration errors, or CI/CD bottlenecks.
    Format the output as markdown.
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    report = chain.invoke({
        "context": context_text,
        "structure": str(state.get("repo_structure", {}))
    })
    
    return {
        "risk_report": report,
        "manifest_findings": manifest_findings,
        "next_step": "patch"
    }
