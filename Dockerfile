FROM python:3.12-slim

# System packages
RUN apt-get update && \
    apt-get install -y curl unzip git gnupg && \
    pip install --upgrade pip

# Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install kube-bench
RUN curl -L https://github.com/aquasecurity/kube-bench/releases/download/v0.6.18/kube-bench_0.6.18_linux_amd64.tar.gz | tar xz && \
    mv kube-bench /usr/local/bin/kube-bench

# Install Trivy
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh && \
    mv ./bin/trivy /usr/local/bin/ && \
    rm -rf ./bin
# Copy everything
WORKDIR /app
COPY . .

# Ensure run_scan.sh is executable
RUN chmod +x /app/run_scan.sh

# Run the scanner
ENTRYPOINT ["./run_scan.sh"]