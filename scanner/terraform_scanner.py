import subprocess
import json

def scan_terraform(path: str) -> dict:
    try:
        result = subprocess.run(
            ["checkov", "-d", path, "-o", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        checkov_output = json.loads(result.stdout)
        issues = []

        for check in checkov_output.get("results", {}).get("failed_checks", []):
            issues.append({
                "file": check.get("file_path"),
                "check_id": check.get("check_id"),
                "check_name": check.get("check_name"),
                "resource": check.get("resource"),
                "severity": check.get("severity", "UNKNOWN"),
                "guideline": check.get("guideline", "")
            })

        return {"terraform": issues}
    except subprocess.CalledProcessError as e:
        print(f"Error running Checkov: {e.stderr}")
        return {"terraform": []}
