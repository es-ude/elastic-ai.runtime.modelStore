# based on https://www.tensorflow.org/tutorials/quickstart/beginner

import mlflow
import tensorflow as tf

import mlflow_tflite
import model_store_client as msc


# start mlflow run

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.start_run()
mlflow.tensorflow.autolog(log_models=False)


# generate training data

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0


# design model

model = tf.keras.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
model.add(tf.keras.layers.Dense(128, activation="relu"))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.Softmax())
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])


# train model and save as SavedModel

MODEL_TF = "models/model"
MODEL_TFLITE = "models/model.tflite"

model.fit(x_train, y_train, epochs=5)
model.save(MODEL_TF)


# convert SavedModel to .tflite format

converter = tf.lite.TFLiteConverter.from_saved_model(MODEL_TF)
model_tflite = converter.convert()

with open(MODEL_TFLITE, "wb") as file:
    file.write(model_tflite)


# log and register model

REG_MODEL_NAME = "digit_classifier"

msc.log_predicate(msc.ServiceNamespace.Predict, msc.ServiceNamespace.Digits)
msc.log_predicate(msc.ServiceNamespace.Input, msc.ServiceNamespace.Float)
msc.log_predicate(msc.ServiceNamespace.Output, msc.ServiceNamespace.Float)
model_info = mlflow_tflite.log_model(model_tflite, "model")
msc.register_model(model_info.model_uri, REG_MODEL_NAME)


# end mlflow run

mlflow.end_run()


# improve model with additional training

mlflow.start_run()
mlflow.tensorflow.autolog(log_models=False)

model.fit(x_train, y_train, epochs=20)
model.save(MODEL_TF)

converter = tf.lite.TFLiteConverter.from_saved_model(MODEL_TF)
model_tflite = converter.convert()

with open(MODEL_TFLITE, "wb") as file:
    file.write(model_tflite)

msc.log_predicate(msc.ServiceNamespace.Predict, msc.ServiceNamespace.Digits)
msc.log_predicate(msc.ServiceNamespace.Input, msc.ServiceNamespace.Float)
msc.log_predicate(msc.ServiceNamespace.Output, msc.ServiceNamespace.Float)
model_info = mlflow_tflite.log_model(model_tflite, "model")
msc.register_model(model_info.model_uri, REG_MODEL_NAME)

mlflow.end_run()
