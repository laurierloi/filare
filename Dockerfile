FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3 python3-venv python3-pip \
      graphviz \
      curl \
      git \
      npm && \
    npm install --global prettier@3 @mermaid-js/mermaid-cli@11.12.0 && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV UV_PROJECT_ENVIRONMENT=/opt/filare/.venv
ENV PATH="/opt/filare/.venv/bin:/root/.local/bin:${PATH}"

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY mkdocs.yml ./
COPY src ./src
COPY tests ./tests
COPY examples ./examples
COPY tutorial ./tutorial
COPY docs ./docs

# Create a project venv with dev deps so lint/tests work in the image
RUN /root/.local/bin/uv venv "$UV_PROJECT_ENVIRONMENT" && \
    UV_PROJECT_ENVIRONMENT="$UV_PROJECT_ENVIRONMENT" /root/.local/bin/uv sync --group dev

CMD ["/bin/bash"]
