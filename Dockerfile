# 运行环境
FROM ubuntu:22.04
# 设置语言环境变量
ENV LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8
# 安装所有必要的软件包和工具
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        wget \
        unzip \
        openssh-server \
        ca-certificates \
        git \
    # 安装 code-server 和扩展
    && curl -fsSL https://code-server.dev/install.sh | sh \
    && code-server --install-extension redhat.vscode-yaml \
    && code-server --install-extension eamodio.gitlens \
    && code-server --install-extension tencent-cloud.coding-copilot \
    && code-server --install-extension golang.go \
    # 安装 Node.js 和 pnpm
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g pnpm \
    && npm cache clean --force \
    # 清理缓存和临时文件
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* /usr/share/man/* /usr/share/info/*
# 安装 Hugo
RUN wget https://github.com/gohugoio/hugo/releases/download/v0.150.0/hugo_extended_0.150.0_Linux-64bit.tar.gz && \
    tar -xzf hugo_extended_0.150.0_Linux-64bit.tar.gz && \
    mv hugo /usr/local/bin/ && \
    rm hugo_extended_0.150.0_Linux-64bit.tar.gz
# 验证安装
RUN hugo version