
from flask import Flask, request, jsonify
import numpy as np
import joblib
import tensorflow as tf

app = Flask(__name__)

# Cargar el modelo y el scaler
modelo = tf.keras.models.load_model("modelo_estres_hidrico_maiz.h5")
scaler = joblib.load("scaler_estres_hidrico_maiz.pkl")

# Mapeo de clases a etiquetas
etiquetas = [
    "Sin Estrés", "Bajo", "Medio", "Medio Alto", "Alto", "Severo"
]

@app.route("/predict", methods=["POST"])
def predecir():
    datos = request.get_json()

    try:
        entradas = np.array([[datos["B4"], datos["B8"], datos["B11"], datos["NDVI"]]])
        entradas_escaladas = scaler.transform(entradas)
        predicciones = modelo.predict(entradas_escaladas)
        clase = int(np.argmax(predicciones))
        return jsonify({
            "clase_estres": clase,
            "etiqueta": etiquetas[clase]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/", methods=["GET"])
def inicio():
    return "API de Predicción de Estrés Hídrico funcionando."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
