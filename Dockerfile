# Lightweight Python runtime for fast, reproducible evaluation
FROM python:3.11-slim

# Prevent Python from writing pyc files to disc and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (leveraging Docker layer cache)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy only required application source code and configuration files
COPY app/ /app/app/
COPY configs/ /app/configs/
COPY main.py rank.py validate_submission.py app.py /app/

# Create data and output directories, and set non-root user for security best practices
RUN mkdir -p /app/data /app/OUTPUT && \
    useradd -m -u 1000 redrob && \
    chown -R redrob:redrob /app

USER redrob

# Default command entry point
ENTRYPOINT ["python", "rank.py"]
CMD ["--help"]
