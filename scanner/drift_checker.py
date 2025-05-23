import subprocess
import json

def load_terraform_plan(plan_json_path):
    with open(plan_json_path) as f:
        return json.load(f)

def detect_drift(plan_data):
    drift_findings = []
    for res in plan_data.get("resource_changes", []):
        if res.get("change", {}).get("actions") == ["update"]:
            drift_findings.append({
                "resource": res["address"],
                "change": res["change"],
                "severity": "MEDIUM",
                "issue": "Terraform drift detected (plan vs actual)"
            })
    return {"drift": drift_findings}