import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, RandomFlip, RandomRotation, RandomZoom, RandomContrast
from tensorflow.keras.models import Model

def main():
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset_cotton")
    img_size = (224, 224)
    batch_size = 16
    epochs = 8

    print("--- Loading Cotton & Pest Dataset ---")
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        base_dir,
        validation_split=0.2,
        subset="training",
        seed=42,
        shuffle=True,
        batch_size=batch_size,
        image_size=img_size,
        label_mode='categorical'
    )

    val_dataset = tf.keras.utils.image_dataset_from_directory(
        base_dir,
        validation_split=0.2,
        subset="validation",
        seed=42,
        shuffle=False,
        batch_size=batch_size,
        image_size=img_size,
        label_mode='categorical'
    )

    class_names = train_dataset.class_names
    num_classes = len(class_names)
    print(f"Detected {num_classes} classes: {class_names}")

    # Standardize class names for Crop Doctor
    # Directory names -> internal class identifiers
    label_mapping = {
        "0_Bollworm": "Cotton___Bollworm",
        "1_Bacterial_Blight": "Cotton___Bacterial_blight",
        "2_Curl_Virus": "Cotton___Curl_virus",
        "3_Healthy": "Cotton___healthy",
        "4_Other_Crop": "Other_Crop"
    }
    standard_class_names = [label_mapping.get(c, c) for c in class_names]

    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")
    os.makedirs(model_dir, exist_ok=True)
    classes_path = os.path.join(model_dir, "cotton_classes.json")
    with open(classes_path, "w") as f:
        json.dump(standard_class_names, f, indent=2)
    print(f"Saved class names to {classes_path}: {standard_class_names}")

    AUTOTUNE = tf.data.AUTOTUNE
    train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
    val_dataset = val_dataset.prefetch(buffer_size=AUTOTUNE)

    # Base MobileNetV2
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False

    # Head layers
    gap_layer = GlobalAveragePooling2D(name="gap")
    dropout_layer = Dropout(0.3, name="drop")
    dense_layer = Dense(128, activation='relu', name="dense_128")
    out_layer = Dense(num_classes, activation='softmax', name="softmax_out")

    # Training graph with augmentation
    train_inputs = tf.keras.Input(shape=(224, 224, 3), name="train_input")
    x = RandomFlip("horizontal_and_vertical")(train_inputs)
    x = RandomRotation(0.2)(x)
    x = RandomZoom(0.15)(x)
    x = RandomContrast(0.1)(x)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    x = base_model(x, training=False)
    x = gap_layer(x)
    x = dropout_layer(x)
    x = dense_layer(x)
    train_outputs = out_layer(x)

    train_model = Model(train_inputs, train_outputs, name="CottonPestClassifier")
    train_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("\n--- Training Stage 1: Transfer Learning ---")
    train_model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=epochs
    )

    print("\n--- Training Stage 2: Fine-Tuning Top Layers ---")
    base_model.trainable = True
    for layer in base_model.layers[:-25]:
        layer.trainable = False

    train_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=2e-5),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    train_model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=3
    )

    val_loss, val_acc = train_model.evaluate(val_dataset)
    print(f"\n[EVAL] Final Validation Accuracy: {val_acc*100:.2f}%, Loss: {val_loss:.4f}")

    print("\n--- Exporting TFLite Model ---")
    inf_inputs = tf.keras.Input(shape=(224, 224, 3), name="image_input")
    inf_x = tf.keras.applications.mobilenet_v2.preprocess_input(inf_inputs)
    inf_x = base_model(inf_x, training=False)
    inf_x = gap_layer(inf_x)
    inf_x = dense_layer(inf_x)
    inf_outputs = out_layer(inf_x)

    inf_model = Model(inf_inputs, inf_outputs, name="CottonPestInference")
    converter = tf.lite.TFLiteConverter.from_keras_model(inf_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    tflite_path = os.path.join(model_dir, "cotton_pest.tflite")
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)

    print(f"[SUCCESS] cotton_pest.tflite saved to: {tflite_path}")
    print(f"Model size: {os.path.getsize(tflite_path) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()
