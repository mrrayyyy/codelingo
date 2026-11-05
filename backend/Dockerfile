FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
COPY backend/requirements.lock ./requirements.lock
RUN pip install --no-cache-dir -r requirements.lock
COPY backend/pyproject.toml ./pyproject.toml
COPY backend/app ./app
COPY backend/tests/fixtures ./tests/fixtures
RUN pip install --no-deps . && useradd --create-home --uid 10001 codelingo && mkdir -p /spool /app/.data && chown -R codelingo:codelingo /spool /app/.data
USER codelingo
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
