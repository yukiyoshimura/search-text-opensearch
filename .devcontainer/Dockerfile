FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /workspace

# システムパッケージの更新とツールのインストール（最小限）
RUN apt-get update && apt-get install -y \
    curl \
    git \
    poppler-utils \
    tesseract-ocr \
    sudo \
    procps \
    dnsutils \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# ユーザーの設定（vscode用）
RUN useradd -m -s /bin/bash vscode && \
    echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    chown -R vscode:vscode /workspace

# Pythonパッケージを更新
RUN pip install --upgrade pip setuptools wheel

# ユーザーを切り替え
USER vscode 