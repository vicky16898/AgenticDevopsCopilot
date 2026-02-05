from typing import List, Dict, Any
import re

class CIInspector:
    def analyze_logs(self, log_content: str) -> Dict[str, Any]:
        """
        Analyzes CI logs for common errors and patterns.
        """
        error_patterns = [
            (r"Error: Process completed with exit code (\d+)", "Process Exit Error"),
            (r"Permission denied", "Permission Issue"),
            (r"Connection refused", "Network/Connection Issue"),
            (r"Time-out|Timed out", "Timeout")
        ]
        
        findings = []
        for pattern, label in error_patterns:
            matches = re.finditer(pattern, log_content, re.IGNORECASE)
            for match in matches:
                findings.append({
                    "type": label,
                    "match": match.group(0),
                    "position": match.start()
                })
                
        return {
            "status": "failed" if findings else "success",
            "findings": findings,
            "log_length": len(log_content)
        }

ci_inspector = CIInspector()
