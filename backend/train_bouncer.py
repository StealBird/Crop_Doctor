import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, RandomFlip, RandomRotation, RandomZoom, RandomContrast
from tensorflow.keras.models import Model

def main():
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
    batch_size = 32
    img_size = (224, 224)
    epochs = 4

    print("Loading training dataset (80%)...")
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        base_dir,
        validation_split=0.2,
        subset="training",
        seed=1337,
        shuffle=True,
        batch_size=batch_size,
        image_size=img_size,
        label_mode='binary'
    )

    print("Loading validation dataset (20%)...")
    val_dataset = tf.keras.utils.image_dataset_from_directory(
        base_dir,
        validation_split=0.2,
        subset="validation",
        seed=1337,
        shuffle=False,
        batch_size=batch_size,
        image_size=img_size,
        label_mode='binary'
    )

    class_names = train_dataset.class_names
    print(f"Detected classes: {class_names} (0: {class_names[0]}, 1: {class_names[1]})")

    AUTOTUNE = tf.data.AUTOTUNE
    train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
    val_dataset = val_dataset.prefetch(buffer_size=AUTOTUNE)

    # Reusable layer instances
    gap_layer = GlobalAveragePooling2D(name="global_avg_pool")
    dropout_layer = Dropout(0.3, name="dropout")
    dense_layer = Dense(64, activation='relu', name="dense_64")
    out_layer = Dense(1, activation='sigmoid', name="leaf_prob")

    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False

    # Training graph with data augmentation
    train_inputs = tf.keras.Input(shape=(224, 224, 3), name="train_input")
    x = RandomFlip("horizontal_and_vertical")(train_inputs)
    x = RandomRotation(0.15)(x)
    x = RandomZoom(0.1)(x)
    x = RandomContrast(0.1)(x)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    x = base_model(x, training=False)
    x = gap_layer(x)
    x = dropout_layer(x)
    x = dense_layer(x)
    train_outputs = out_layer(x)

    train_model = Model(train_inputs, train_outputs, name="CropDoctorBouncerTrain")
    train_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    print("\nStarting Training Bouncer Model on Real Datasets...")
    train_model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=epochs
    )

    # Fine-tuning: unfreeze last 20 layers of MobileNetV2
    print("\nFine-tuning top layers of MobileNetV2...")
    base_model.trainable = True
    for layer in base_model.layers[:-20]:
        layer.trainable = False

    train_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=2e-5),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    train_model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=2
    )

    loss, acc = train_model.evaluate(val_dataset)
    print(f"\nFinal Validation Accuracy: {acc*100:.2f}%, Loss: {loss:.4f}")

    print("\nExporting as lightweight TFLite model...")
    # Inference graph without data augmentation
    inf_inputs = tf.keras.Input(shape=(224, 224, 3), name="image_input")
    inf_x = tf.keras.applications.mobilenet_v2.preprocess_input(inf_inputs)
    inf_x = base_model(inf_x, training=False)
    inf_x = gap_layer(inf_x)
    inf_x = dense_layer(inf_x)
    inf_outputs = out_layer(inf_x)

    inference_model = Model(inf_inputs, inf_outputs, name="BouncerInference")

    converter = tf.lite.TFLiteConverter.from_keras_model(inference_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")
    os.makedirs(model_dir, exist_ok=True)
    tflite_path = os.path.join(model_dir, "bouncer.tflite")
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)

    print(f"[SUCCESS] Bouncer model saved successfully to: {tflite_path}")
    print(f"Model size: {os.path.getsize(tflite_path) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()
