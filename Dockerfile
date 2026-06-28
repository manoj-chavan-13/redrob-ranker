# Lightweight Python runtime for fast, reproducible evaluation
FROM python:3.11-slim

# Prevent Python from writing pyc files to disc and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the ranking script and validator into the container
COPY rank.py validate_submission.py /app/

# Set non-root user for security best practices
RUN useradd -m -u 1000 redrob && chown -R redrob:redrob /app
USER redrob

# Default command entry point
ENTRYPOINT ["python", "rank.py"]
CMD ["--help"]
