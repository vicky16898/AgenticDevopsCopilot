from app.agents.state import AgentState
from app.mcp_servers.repo_parser import repo_parser
from app.rag.ingestion import rag_ingestor

def analyze_repo_node(state: AgentState) -> dict:
    """
    1. Parses the repo at state['repo_path']
    2. Ingests code into Qdrant
    3. Returns structure and file list
    """
    repo_path = state.get("repo_path", ".")
    print(f"--- Analyzing Repo: {repo_path} ---")
    
    # Handle GitHub URLs
    if repo_path.startswith(("http://", "https://")):
        import tempfile
        import subprocess
        import shutil
        
        repo_name = repo_path.split("/")[-1].replace(".git", "")
        # Create a temp dir (or use a persistent cache dir if preferred)
        # For simplicity, we clone into a temp folder
        temp_dir = tempfile.mkdtemp()
        try:
            print(f"Cloning {repo_path} to {temp_dir}...")
            subprocess.run(["git", "clone", repo_path, temp_dir], check=True)
            target_path = temp_dir
        except Exception as e:
            return {"error": f"Failed to clone repo: {e}", "next_step": "end"}
    else:
        target_path = repo_path

    # 1. Update Parser Root
    from pathlib import Path
    repo_parser.root_path = Path(target_path).resolve()
    # For this simplified version, we assume path is handled or passed
    
    # 2. Get Structure
    structure = repo_parser.get_structure()
    
    # 3. Extract Files
    files = repo_parser.extract_files()
    
    # 4. Ingest into RAG
    print(f"Ingesting {len(files)} files into RAG...")
    rag_ingestor.ingest_files(files)
    
    
    analyzed_paths = [f['path'] for f in files]
    
    return {
        "repo_structure": structure,
        "analyzed_files": analyzed_paths,
        "repo_path": repo_path,
        "next_step": "risk",
        "cleanup_path": target_path if repo_path.startswith(("http://", "https://")) else None
    }
