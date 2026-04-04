FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gdown==5.2.1

# Download model at build time
RUN mkdir -p model && gdown --fuzzy "1D5Jv5B7kl5VBhWFna4sPzT6gwVk2HL-T" -O model/model.tflite

COPY . .

RUN chmod +x startup.sh
CMD ["./startup.sh"]