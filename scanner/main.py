import argparse
import os
from terraform_scanner import scan_terraform
from azure_scanner import scan_azure
from report_generator import generate_report
from kubernetes_scanner import scan_kubernetes
from rbac_scanner import scan_rbac
from config_loader import load_config
from drift_checker import detect_drift, load_terraform_plan

def main():
    parser = argparse.ArgumentParser(description="Qrypsis - Infrastructure Compliance Scanner")
    parser.add_argument('--terraform', type=str, help='Path to Terraform directory')
    parser.add_argument('--azure', action='store_true', help='Scan Azure Key Vaults and ACR')
    parser.add_argument('--kube', action='store_true', help='Scan Kubernetes cluster runtime')
    parser.add_argument('--rbac', action='store_true', help='Scan Kubernetes RBAC permissions')
    parser.add_argument('--drift', action='store_true', help='Run Terraform drift detection using plan.json')
    parser.add_argument('--fail-on', type=str, help='Fail if issues of this severity are found (LOW, MEDIUM, HIGH)')
    parser.add_argument('--exit-code', action='store_true', help='Return non-zero code on critical issues')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--no-redact', action='store_true', help='Disable secret redaction')
    args = parser.parse_args()

    results = []

    # Load config.yaml if specified
    if args.config:
        config = load_config(args.config)
        if config.get("terraform"):
            args.terraform = config["terraform"].get("path")
        if config.get("azure"):
            args.azure = config["azure"].get("enabled", False)
        if config.get("kubernetes"):
            args.kube = config["kubernetes"].get("enabled", False)
        if config.get("rbac"):
            args.rbac = config["rbac"].get("enabled", False)
        if config.get("fail_on"):
            args.fail_on = config["fail_on"]
        if config.get("drift"):
            args.drift = config["drift"].get("enabled", False)

    # Run scanners
    if args.terraform:
        print(f"📁 Scanning Terraform code at {args.terraform}")
        results.append(scan_terraform(args.terraform))

    if args.azure:
        print("🔍 Scanning Azure Key Vault & ACR...")
        results.append(scan_azure(redact=not args.no_redact))

    if args.kube:
        print("☸️  Scanning Kubernetes cluster...")
        results.append(scan_kubernetes())

    if args.rbac:
        print("🔐 Scanning Kubernetes RBAC...")
        results.append(scan_rbac())

    # Optional drift detection
    if args.drift:
        if not os.path.exists("plan.json"):
            print("⚠️  Skipping drift detection: plan.json not found.")
        else:
            print("📊 Running Terraform drift detection...")
            plan_data = load_terraform_plan("plan.json")
            results.append(detect_drift(plan_data))

    # Generate report
    generate_report(results)

    # Severity threshold enforcement
    if args.fail_on:
        fail = False
        for section in results:
            for layer in section.values():
                for issue in layer:
                    if issue.get("severity", "").upper() == args.fail_on.upper():
                        fail = True
        if fail:
            print(f"❌ Compliance failed due to {args.fail_on} findings")
            exit(1)

if __name__ == "__main__":
    main()