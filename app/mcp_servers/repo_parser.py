import os
from typing import List, Dict, Any
from pathlib import Path

class RepoParser:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()

    def get_structure(self, max_depth: int = 3) -> Dict[str, Any]:
        """Returns a nested dictionary representing the file structure."""
        def build_tree(path: Path, current_depth: int) -> Dict[str, Any]:
            if current_depth > max_depth:
                return {}
            
            tree = {}
            try:
                for item in path.iterdir():
                    if item.name.startswith(('.', '__')) or item.name in ['node_modules', 'venv', 'env', 'dist', 'build', 'target']:
                        continue
                        
                    if item.is_dir():
                        tree[item.name] = build_tree(item, current_depth + 1)
                    else:
                        tree[item.name] = "file"
            except PermissionError:
                pass
            return tree

        return build_tree(self.root_path, 0)

    def extract_files(self, extensions: List[str] = ['.py', '.yaml', '.yml', '.json', '.md']) -> List[Dict[str, str]]:
        """Extracts content from files with matching extensions."""
        results = []
        for path in self.root_path.rglob('*'):
            if path.is_file() and path.suffix in extensions and not any(p.startswith('.') for p in path.parts):
                try:
                    content = path.read_text(encoding='utf-8', errors='ignore')
                    results.append({
                        "path": str(path.relative_to(self.root_path)),
                        "content": content,
                        "extension": path.suffix
                    })
                except Exception as e:
                    print(f"Error reading {path}: {e}")
        return results

repo_parser = RepoParser()
