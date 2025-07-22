import numpy as np
import joblib
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# === CARGAR MODELO Y ESCALADOR ===
modelo = tf.keras.models.load_model("modelo_estres_hidrico_maiz_vfinal.keras")
scaler = joblib.load("scaler_estres_hidrico_maiz_vfinal.pkl")

@app.route("/", methods=["GET"])
def index():
    return "API de Predicción de Estrés Hídrico Activa."

@app.route("/predecir", methods=["POST"])
def predecir():
    try:
        datos = request.get_json()
        variables = np.array(datos["variables"]).reshape(1, -1)
        variables_escaladas = scaler.transform(variables)
        prediccion = modelo.predict(variables_escaladas)
        clase_predicha = int(np.argmax(prediccion))
        confianza = float(np.max(prediccion))
        return jsonify({"clase_predicha": clase_predicha, "confianza": confianza})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
