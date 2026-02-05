from typing import List, Dict, Any
import yaml

class K8sValidator:
    def validate_manifest(self, content: str) -> List[Dict[str, Any]]:
        """
        Validates k8s manifests via simple schema checks (placeholder for kubeval).
        Returns a list of finding dictionaries.
        """
        findings = []
        try:
            documents = yaml.safe_load_all(content)
            for doc in documents:
                if not doc:
                    continue
                
                kind = doc.get("kind")
                metadata = doc.get("metadata", {})
                name = metadata.get("name", "unknown")
                
                # Example Check: Enforce requests/limits
                if kind in ["Deployment", "StatefulSet", "DaemonSet"]:
                    containers = doc.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
                    for container in containers:
                        resources = container.get("resources", {})
                        if not resources.get("limits") or not resources.get("requests"):
                            findings.append({
                                "severity": "medium",
                                "message": f"Container '{container.get('name')}' in {kind}/{name} is missing resource limits/requests.",
                                "resource": f"{kind}/{name}"
                            })
                            
                # Example Check: Image Tag should not be 'latest'
                if kind in ["Deployment", "Pod"]:
                     containers = doc.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
                     if not containers: # Handle direct Pod spec
                         containers = doc.get("spec", {}).get("containers", [])
                         
                     for container in containers:
                         image = container.get("image", "")
                         if image.endswith(":latest") or ":" not in image:
                             findings.append({
                                 "severity": "high",
                                 "message": f"Container '{container.get('name')}' uses 'latest' or mutable image tag.",
                                 "resource": f"{kind}/{name}"
                             })

        except yaml.YAMLError as e:
            findings.append({"severity": "critical", "message": f"Invalid YAML: {str(e)}", "resource": "n/a"})
            
        return findings

k8s_validator = K8sValidator()
