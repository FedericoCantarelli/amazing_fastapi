FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

# Copy the application into the container.
COPY ./app /code/app
COPY ./run.py /code/run.py
COPY ./pyproject.toml /code/pyproject.toml
COPY ./uv.lock /code/uv.lock

# Install the application dependencies.
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["/code/.venv/bin/python", "run.py"]