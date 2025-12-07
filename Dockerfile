FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install OS deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY Pipfile Pipfile.lock* requirements.txt* /app/

# If using pipenv:
# RUN pip install pipenv && pipenv install --system --deploy

# If using requirements.txt (preferred)
RUN pip install --upgrade pip
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy the project
COPY . .

# Collect static files if you want (needs STATIC_ROOT in settings)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Revitage.wsgi:application"]