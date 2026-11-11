FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser
COPY . .
RUN chown -R appuser:appgroup /app
USER appuser

CMD ["python3", "main.py"]
