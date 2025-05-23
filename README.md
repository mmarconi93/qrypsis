![CI](https://github.com/mmarconi93/qrypsis/actions/workflows/scan.yaml/badge.svg)

# Qrypsis

Qrypsis is a modern, DevOps-first compliance scanner for Kubernetes, Terraform, and Azure.  
It detects misconfigurations, cloud drift, and security policy violations — and generates clean, actionable reports in Markdown, HTML, or PDF.

---

## 🚀 Features

- ✅ **Terraform** compliance scanning with Checkov
- 🔐 **Azure** Key Vault, ACR, NSG checks
- ☸️ **Kubernetes** runtime + RBAC scanning (Trivy + kube-bench)
- 🧾 Markdown, HTML, and PDF **audit reports**
- 🔄 Terraform **drift detection**
- 🧪 Redact secrets, fail CI/CD on high severity
- 🔧 Fully **configurable** via YAML file

---

## ⚡ Quick Start

```bash
git clone https://github.com/mmarconi93/qrypsis.git
cd qrypsis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with default config file
./run_scan.sh

# Or specify manually
python3 scanner/main.py --terraform ./examples/iac/ --azure --kube --fail-on HIGH

## What We Scan

- 🔐 Azure Key Vault: Public access, expiring secrets
- 📦 Azure ACR: Admin access, public access
- 🌐 Azure NSG: Open ports from 0.0.0.0/0
- ⚙️ Kubernetes: kube-bench + Trivy + RBAC
- 🔄 Terraform: Misconfigs + Drift detection

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](./LICENSE) file for details.