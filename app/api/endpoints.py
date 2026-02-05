from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.agents.graph import app_graph

router = APIRouter()

class AnalyzeRequest(BaseModel):
    repo_path: str

class AnalysisResponse(BaseModel):
    status: str
    risk_report: str
    patches: List[Dict[str, Any]]
    analyzed_files: List[str]

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_repository(request: AnalyzeRequest):
    """
    Triggers the DevOps Copilot agent to analyze a repository.
    """
    try:
        # Initial State
        initial_state = {
            "messages": [],
            "repo_path": request.repo_path,
            "repo_structure": {},
            "analyzed_files": [],
            "manifest_findings": [],
            "ci_issues": [],
            "risk_report": "",
            "proposed_patches": [],
            "next_step": "start",
            "error": None
        }
        
        # Invoke Graph (Synchronous for MVP)
        result = app_graph.invoke(initial_state)
        
        # Cleanup Temp Dir if needed
        cleanup_path = result.get("cleanup_path")
        if cleanup_path:
            import shutil
            import os
            try:
                if os.path.exists(cleanup_path):
                    shutil.rmtree(cleanup_path)
                    print(f"Cleaned up temp repo: {cleanup_path}")
            except Exception as e:
                print(f"Failed to cleanup temp dir: {e}")

        return AnalysisResponse(
            status="success",
            risk_report=result.get("risk_report", "No report generated."),
            patches=result.get("proposed_patches", []),
            analyzed_files=result.get("analyzed_files", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
