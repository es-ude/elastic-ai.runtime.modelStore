# based on https://colab.research.google.com/github/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/examples/hello_world/train/train_hello_world_model.ipynb

import math
import mlflow
import mlflow_tflite
import numpy as np
import tensorflow as tf


# start mlflow run

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.start_run()


# generate training data

SAMPLES = 1000

x_values = np.random.uniform(low=0, high=2 * math.pi, size=SAMPLES).astype(np.float32)
np.random.shuffle(x_values)
y_values = np.sin(x_values).astype(np.float32)

y_values += 0.1 * np.random.randn(*y_values.shape)


# split data

TRAIN_SPLIT = int(0.6 * SAMPLES)  # 60%
TEST_SPLIT = int(0.2 * SAMPLES + TRAIN_SPLIT)  # 20%

x_train, x_test, x_validate = np.split(x_values, [TRAIN_SPLIT, TEST_SPLIT])
y_train, y_test, y_validate = np.split(y_values, [TRAIN_SPLIT, TEST_SPLIT])


# design model

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(16, activation="relu", input_shape=(1,)))
model.add(tf.keras.layers.Dense(16, activation="relu"))
model.add(tf.keras.layers.Dense(1))
model.compile(optimizer="adam", loss="mse", metrics=["mae"])


# train model and save as SavedModel

MODEL_TF = "models/model"
MODEL_TFLITE = "models/model.tflite"

model.fit(x_train, y_train, epochs=500, batch_size=64, validation_data=(x_validate, y_validate))
model.save(MODEL_TF)


# convert SavedModel to .tflite format (with quantization)

def representative_dataset():
   for i in range(500):
      yield([x_train[i].reshape(1, 1)])

converter = tf.lite.TFLiteConverter.from_saved_model(MODEL_TF)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8
converter.representative_dataset = representative_dataset
model_tflite = converter.convert()

with open(MODEL_TFLITE, "wb") as f:
   f.write(model_tflite)


# log and register model

REG_MODEL_NAME = "hello_world_trained"

mlflow_tflite.log_model(model_tflite, "model", registered_model_name=REG_MODEL_NAME)


# end mlflow run

mlflow.end_run()
