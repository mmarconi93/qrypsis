FROM python:3.12-slim

# System packages
RUN apt-get update && \
    apt-get install -y curl unzip git gnupg ca-certificates && \
    pip install --upgrade pip

# Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install kube-bench
RUN curl -L https://github.com/aquasecurity/kube-bench/releases/download/v0.6.18/kube-bench_0.6.18_linux_amd64.tar.gz | tar xz && \
    mv kube-bench /usr/local/bin/kube-bench

# Install Trivy using release binary directly
RUN curl -L https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.62.1_Linux-64bit.tar.gz | \
    tar -zxvf - -C /usr/local/bin trivy

WORKDIR /app
COPY . .

# Ensure run_scan.sh is executable
RUN chmod +x /app/run_scan.sh

# Run the scanner
ENTRYPOINT ["./run_scan.sh"]
