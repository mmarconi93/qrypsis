FROM python:3.12-slim

# System packages
RUN apt-get update && \
    apt-get install -y curl unzip git gnupg && \
    pip install --upgrade pip

# Install Python dependencies
RUN pip install checkov jinja2 kubernetes azure-identity azure-mgmt-keyvault azure-mgmt-resource azure-mgmt-containerregistry azure-keyvault-secrets

# Install kube-bench
RUN curl -L https://github.com/aquasecurity/kube-bench/releases/download/v0.6.18/kube-bench_0.6.18_linux_amd64.tar.gz | tar xz && \
    mv kube-bench /usr/local/bin/kube-bench

# Install Trivy
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh && \
    mv trivy /usr/local/bin/

WORKDIR /app
COPY . .

CMD ["python", "scanner/main.py"]
