# Qrypsis

Qrypsis is a modern DevOps-first compliance scanner for Kubernetes, Terraform, and Azure. It detects misconfigurations, drift, and compliance violations and generates clean, actionable reports.

## Features

- ✅ Terraform compliance scanning with Checkov
- 📄 Markdown reports (PDF export coming soon)
- ☁️ Azure and Kubernetes support (WIP)

## Quick Start

```bash
git clone https://github.com/your-org/qrypsis.git
cd qrypsis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python scanner/main.py --terraform ./examples/iac/
