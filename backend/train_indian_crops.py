import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, RandomFlip, RandomRotation, RandomZoom, RandomContrast
from tensorflow.keras.models import Model

def main():
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset_indian")
    img_size = (224, 224)
    batch_size = 32
    epochs_stage1 = 6
    epochs_stage2 = 3

    print("--- Loading Top 10 Indian Crops Dataset ---")
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
    print(f"\n[INFO] Detected {num_classes} Indian Crop Classes:")
    for idx, c in enumerate(class_names):
        print(f"  {idx:02d}: {c}")

    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")
    os.makedirs(model_dir, exist_ok=True)
    classes_path = os.path.join(model_dir, "indian_classes.json")
    with open(classes_path, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)
    print(f"\nSaved class list to: {classes_path}")

    AUTOTUNE = tf.data.AUTOTUNE
    train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
    val_dataset = val_dataset.prefetch(buffer_size=AUTOTUNE)

    # Base MobileNetV2 architecture
    print("\n--- Initializing MobileNetV2 with ImageNet Weights ---")
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False

    # Head layers
    gap_layer = GlobalAveragePooling2D(name="gap")
    dropout_layer = Dropout(0.35, name="drop")
    dense_layer = Dense(256, activation='relu', name="dense_256")
    dropout_2 = Dropout(0.2, name="drop_2")
    out_layer = Dense(num_classes, activation='softmax', name="softmax_out")

    # Training graph with real field data augmentation
    train_inputs = tf.keras.Input(shape=(224, 224, 3), name="train_input")
    x = RandomFlip("horizontal_and_vertical")(train_inputs)
    x = RandomRotation(0.25)(x)
    x = RandomZoom(0.20)(x)
    x = RandomContrast(0.15)(x)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    x = base_model(x, training=False)
    x = gap_layer(x)
    x = dropout_layer(x)
    x = dense_layer(x)
    x = dropout_2(x)
    train_outputs = out_layer(x)

    train_model = Model(train_inputs, train_outputs, name="IndianCropsClassifier")
    train_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0006),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("\n--- Training Stage 1: Transfer Learning (Base Frozen) ---")
    train_model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=epochs_stage1
    )

    print("\n--- Training Stage 2: Fine-Tuning Top 30 MobileNetV2 Layers ---")
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    train_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=2e-5),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    train_model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=epochs_stage2
    )

    val_loss, val_acc = train_model.evaluate(val_dataset)
    print(f"\n[EVAL] Final Validation Accuracy: {val_acc*100:.2f}%, Loss: {val_loss:.4f}")

    print("\n--- Exporting Quantized TFLite Model ---")
    # Clean inference graph without dropout/augmentation
    inf_inputs = tf.keras.Input(shape=(224, 224, 3), name="image_input")
    inf_x = tf.keras.applications.mobilenet_v2.preprocess_input(inf_inputs)
    inf_x = base_model(inf_x, training=False)
    inf_x = gap_layer(inf_x)
    inf_x = dense_layer(inf_x)
    inf_outputs = out_layer(inf_x)

    inf_model = Model(inf_inputs, inf_outputs, name="IndianCropsInference")
    converter = tf.lite.TFLiteConverter.from_keras_model(inf_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    tflite_path = os.path.join(model_dir, "indian_crops.tflite")
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)

    size_mb = os.path.getsize(tflite_path) / 1024 / 1024
    print(f"\n[SUCCESS] Exported indian_crops.tflite: {tflite_path}")
    print(f"[SUCCESS] Model Size: {size_mb:.2f} MB (Target: <= 3.5 MB)")

if __name__ == "__main__":
    main()
