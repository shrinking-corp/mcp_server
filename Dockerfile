FROM python:3.12-slim

# prevent prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# install git in order to install pip dependencies from git (shrinking-algorithms)
RUN apt-get update && apt-get install -y --no-install-recommends \
  git \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir .

COPY server.py ./
COPY configs ./configs

CMD ["python", "server.py"]

