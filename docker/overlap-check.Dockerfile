# Playwright-ready image to run the text overlap checker consistently in CI and locally.
FROM mcr.microsoft.com/playwright/python:v1.56.0-jammy

WORKDIR /workspace

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    echo "$HOME/.local/bin" >> /etc/environment

COPY pyproject.toml uv.lock ./
COPY src ./src

RUN uv venv && uv sync --group dev

ENTRYPOINT ["uv", "run", "filare-check-overlap"]
