import subprocess
import json

def scan_kubernetes():
    results = {
        "kube_bench": [],
        "trivy": []
    }

    # Run kube-bench (CIS checks)
    try:
        kube_bench_proc = subprocess.run(
            ["kube-bench", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        kube_bench_output = json.loads(kube_bench_proc.stdout)

        for section in kube_bench_output.get("Controls", {}).get("tests", []):
            for check in section.get("results", []):
                if check["status"] == "FAIL":
                    results["kube_bench"].append({
                        "id": check["test_number"],
                        "description": check["test_desc"],
                        "severity": section.get("severity", "Unknown")
                    })
    except subprocess.CalledProcessError as e:
        results["kube_bench"].append({
            "error": f"Failed to run kube-bench: {e.stderr}"
        })

    # Run Trivy scan on all running pods
    try:
        trivy_proc = subprocess.run(
            ["trivy", "kubernetes", "--report", "summary", "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        trivy_output = json.loads(trivy_proc.stdout)

        for resource in trivy_output.get("ClusterResults", []):
            for result in resource.get("Results", []):
                if result.get("Misconfigurations"):
                    for misconfig in result["Misconfigurations"]:
                        results["trivy"].append({
                            "namespace": resource.get("Namespace"),
                            "resource": resource.get("Target"),
                            "check_id": misconfig.get("ID"),
                            "title": misconfig.get("Title"),
                            "severity": misconfig.get("Severity"),
                            "message": misconfig.get("Message")
                        })
    except subprocess.CalledProcessError as e:
        results["trivy"].append({
            "error": f"Failed to run Trivy: {e.stderr}"
        })

    return {"kubernetes": results}
