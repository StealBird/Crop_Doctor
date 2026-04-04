FROM python:3.11-slim

WORKDIR /app

# Need unzip for extracting the downloaded zip file
RUN apt-get update && apt-get install -y wget unzip && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gdown==5.2.1

# 1. Download custom crop disease model via Google Drive
RUN mkdir -p model && gdown "1D5Jv5B7kl5VBhWFna4sPzT6gwVk2HL-T" -O model/model.tflite

# 2. Download ImageNet MobileNetV1 Quantized and labels for the valid crop gate
RUN wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/mobilenet_v1_1.0_224_quant_and_labels.zip -O /tmp/mobilenet.zip && \
    unzip /tmp/mobilenet.zip -d /tmp/mobilenet && \
    cp /tmp/mobilenet/mobilenet_v1_1.0_224_quant.tflite model/mobilenet_v1.tflite && \
    cp /tmp/mobilenet/labels_mobilenet_quant_v1_224.txt model/imagenet_labels.txt && \
    rm -rf /tmp/mobilenet.zip /tmp/mobilenet

COPY . .

RUN chmod +x startup.sh
CMD ["./startup.sh"]