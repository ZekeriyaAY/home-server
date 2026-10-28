FROM debian:trixie-slim

# Headless browser for agent tasks: Node + Playwright + Chromium (with system deps).
# Browsers live outside /home/claude so the image works regardless of volume mounts.
ARG PLAYWRIGHT_VERSION=1.56.1
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
    NODE_PATH=/usr/local/lib/node_modules

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git ripgrep tini nodejs npm \
    && npm install -g playwright@${PLAYWRIGHT_VERSION} \
    && playwright install --with-deps chromium \
    && npm cache clean --force \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 -s /bin/bash claude

USER claude
WORKDIR /home/claude
RUN curl -fsSL https://claude.ai/install.sh -o /tmp/install.sh \
    && bash /tmp/install.sh \
    && rm /tmp/install.sh \
    && ~/.local/bin/claude --version

ENV PATH=/home/claude/.local/bin:$PATH \
    CLAUDE_CONFIG_DIR=/home/claude/.claude

COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint.sh

WORKDIR /workspace
ENTRYPOINT ["tini", "-g", "--", "entrypoint.sh"]
