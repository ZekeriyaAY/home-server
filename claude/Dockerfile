FROM debian:trixie-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git ripgrep tini \
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
