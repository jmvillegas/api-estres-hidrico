
from flask import Flask, request, jsonify
import numpy as np
import joblib
import tensorflow as tf

app = Flask(__name__)

# Cargar el modelo y el scaler
modelo = tf.keras.models.load_model("modelo_estres_hidrico_maizV8.h5")
scaler = joblib.load("scaler_estres_hidrico_maizV6.pkl")

# Mapeo de clases a etiquetas
etiquetas = [
    "Sin Estrés", "Bajo", "Medio", "Medio Alto", "Alto", "Severo"
]

@app.route("/predict", methods=["POST"])
def predecir():
    datos = request.get_json()

    try:
        campos = ['NDVI_mean', 'NDWI_mean', 'NMDI_mean', 'B4_mean', 'B8_mean', 'B11_mean', 'B12_mean', 'Area_m2']
        entradas = np.array([[datos[c] for c in campos]])

        entradas_escaladas = scaler.transform(entradas)
        predicciones = modelo.predict(entradas_escaladas)
        clase = int(np.argmax(predicciones))

        return jsonify({
            "clase_estres": clase,
            "etiqueta": etiquetas[clase],
            "confianza": float(np.max(predicciones))
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/", methods=["GET"])
def inicio():
    return "API de Predicción de Estrés Hídrico funcionando."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
