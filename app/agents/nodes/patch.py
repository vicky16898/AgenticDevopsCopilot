from app.agents.state import AgentState
from app.core.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

def generate_patch_node(state: AgentState) -> dict:
    """
    Generates proposed code patches based on the risk report.
    """
    print("--- Generating Patches ---")
    
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_template("""
    Based on the following Risk Report, suggest concrete code patches for the most critical issues.
    
    Risk Report:
    {report}
    
    Output Format:
    Return a JSON list of objects with 'file_path', 'explanation', and 'patched_content'.
    Do not output markdown formatting for the JSON, just the raw JSON string.
    """)
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({"report": state["risk_report"]})
        # Clean up potential markdown code blocks if the LLM adds them
        clean_result = result.replace("```json", "").replace("```", "").strip()
        patches = json.loads(clean_result)
    except Exception as e:
        print(f"Error generating patches: {e}")
        patches = []
        
    return {
        "proposed_patches": patches,
        "next_step": "end"
    }
