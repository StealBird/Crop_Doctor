#!/bin/bash
echo "Starting Crop Doctor..."
if [ ! -f "model/model.tflite" ]; then
    echo "Downloading model from Google Drive..."
    mkdir -p model
    pip install gdown -q
    gdown --id 1D5Jv5B7kl5VBhWFna4sPzT6gwVk2HL-T -O model/model.tflite
    echo "Model ready!"
fi
uvicorn main:app --host 0.0.0.0 --port 8000