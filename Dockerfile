# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Best to set these early
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory early
WORKDIR /app

# Install only minimal system packages (remove build-essential if not needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (very common best practice)
RUN useradd -m -u 1000 appuser

# Copy and install dependencies first (great caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create data folder and give ownership to non-root user
RUN mkdir -p /app/data && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8501

# Healthcheck (optional but useful)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run (as non-root)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]