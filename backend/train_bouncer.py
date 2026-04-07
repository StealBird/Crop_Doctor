import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model

def main():
    base_dir = "dataset"
    batch_size = 8
    img_size = (224, 224)
    epochs = 2  # Very low epochs just for proof-of-concept

    print("Loading dataset...")
    # The dataset uses directory names '0_garbage' and '1_leaf'
    # class_names will be inferred as ['0_garbage', '1_leaf'] if sorted alphabetically.
    # Therefore, 0 corresponds to 0_garbage, 1 corresponds to 1_leaf.
    
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        base_dir,
        shuffle=True,
        batch_size=batch_size,
        image_size=img_size,
        label_mode='binary'
    )
    
    # Check classes
    class_names = train_dataset.class_names
    print(f"Detected classes: {class_names}")

    # Build the MobileNetV2 base
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False  # Freeze base model

    # Add custom head
    # MobileNetV2 expects inputs in range [-1, 1]
    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base_model(x, training=False)
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.2)(x)
    outputs = Dense(1, activation='sigmoid')(x)
    model = Model(inputs, outputs)

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    print("Training Bouncer Model...")
    model.fit(train_dataset, epochs=epochs)

    print("Exporting as TFLite model...")
    # We will save model and then convert
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    os.makedirs("model", exist_ok=True)
    tflite_path = "model/bouncer.tflite"
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)
    
    print(f"Bouncer model saved to {tflite_path}")

if __name__ == "__main__":
    main()
