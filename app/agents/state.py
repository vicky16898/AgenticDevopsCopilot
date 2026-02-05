from typing import TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage
import operator
from typing import Annotated

class AgentState(TypedDict):
    # Chat History
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Input Context
    repo_path: str
    
    # Analysis Artifacts
    repo_structure: Optional[Dict[str, Any]]
    analyzed_files: List[str]
    
    # Findings
    manifest_findings: List[Dict[str, Any]]
    ci_issues: List[Dict[str, Any]]
    
    # Generated Outputs
    risk_report: str
    proposed_patches: List[Dict[str, str]] # path -> content
    
    # Internal Flow Control
    next_step: str
    error: Optional[str]
    cleanup_path: Optional[str]
