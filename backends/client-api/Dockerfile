# 1. Python image'ı alıyoruz
FROM python:3.10-slim

# 2. Çalışma dizinini ayarlıyoruz
WORKDIR /app

# 3. requirements.txt'i container'a kopyalıyoruz
COPY requirements.txt requirements.txt

# 4. Gerekli bağımlılıkları yüklüyoruz
RUN pip install --no-cache-dir -r requirements.txt

# 5. Uvicorn sunucusunu çalıştırıyoruz
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
