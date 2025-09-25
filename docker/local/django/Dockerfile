FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS python

ARG APP_HOME=/app

WORKDIR ${APP_HOME}

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gettext \
    wait-for-it

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --no-install-project

COPY . ${APP_HOME}

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync
    

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano

RUN groupadd --gid 1000 dev-user \
    && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
    && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
    && chmod 0440 /etc/sudoers.d/dev-user

ENV PATH="${APP_HOME}/.venv/bin:$PATH"
ENV PYTHONPATH="${APP_HOME}/.venv/lib/python3.13/site-packages:${PYTHONPATH}"

COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/local/django/start-celeryworker /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

ENTRYPOINT [ "/entrypoint" ]