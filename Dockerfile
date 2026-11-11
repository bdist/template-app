# Copyright (c) BDist Development Team
# Distributed under the terms of the Modified BSD License.
ARG PYTHON_VERSION=3.14
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-trixie

LABEL maintainer="Flavio Martins <flavio.f.martins@tecnico.ulisboa.pt>"

# Run the application as an unprivileged user instead of root.
RUN groupadd --system app && useradd --system --gid app --home-dir /app --no-create-home app

# Copy dependency metadata first so app source changes do not invalidate this layer.
COPY pyproject.toml uv.lock /app/

# Compile installed Python modules to reduce application startup time.
ENV UV_COMPILE_BYTECODE=1

# Install locked runtime dependencies and the optional fast extra without development groups.
RUN uv sync --project /app --locked --no-dev --extra fast --no-cache

# Add application source after installing dependencies to preserve the dependency cache.
COPY --chown=app:app . /app

RUN chmod +x /app/entrypoint /app/start

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Configure Python for the application runtime.

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Drop root privileges for the application process.
USER app

WORKDIR /app

ENTRYPOINT [ "/app/entrypoint" ]

CMD [ "/app/start" ]
