FROM python:3.12-slim

# supaya python ga bikin cache pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# install system package seperlunya lalu langsung bersihkan cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# copy requirements dulu agar cache build efisien
COPY requirements.txt .

# install python package tanpa cache
RUN pip install --no-cache-dir -r requirements.txt

# baru copy semua project
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
