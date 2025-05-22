import argparse
from terraform_scanner import scan_terraform
from azure_scanner import scan_azure
from report_generator import generate_report
from kubernetes_scanner import scan_kubernetes
from rbac_scanner import scan_rbac

def main():
    parser = argparse.ArgumentParser(description="Qrypsis - Infrastructure Compliance Scanner")
    parser.add_argument('--terraform', type=str, help='Path to Terraform directory')
    parser.add_argument('--azure', action='store_true', help='Scan Azure Key Vaults and secrets')
    parser.add_argument('--kube', action='store_true', help='Scan Kubernetes cluster runtime')
    parser.add_argument('--rbac', action='store_true', help='Scan Kubernetes RBAC permissions')
    parser.add_argument('--exit-code', action='store_true', help='Return non-zero code on critical issues')
    args = parser.parse_args()

    results = []

    if args.terraform:
        print(f"📁 Scanning Terraform code at {args.terraform}")
        results.append(scan_terraform(args.terraform))

    if args.azure:
        print("🔍 Scanning Azure Key Vault...")
        results.append(scan_azure())

    if args.kube:
        print("☸️  Scanning Kubernetes cluster...")
        results.append(scan_kubernetes())
    
    if args.rbac:
        print("🔐 Scanning Kubernetes RBAC...")
        results.append(scan_rbac())

    generate_report(results)

if __name__ == "__main__":
    main()