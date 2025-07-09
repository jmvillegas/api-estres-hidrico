{\rtf1\ansi\ansicpg1252\cocoartf2759
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from flask import Flask, request, jsonify\
from tensorflow.keras.models import load_model\
import joblib\
import numpy as np\
\
app = Flask(__name__)\
\
# Cargar modelo y escalador\
model = load_model('modelo_estres_hidrico_maiz.h5')\
scaler = joblib.load('scaler_estres_hidrico_maiz.pkl')\
\
@app.route('/predecir', methods=['POST'])\
def predecir():\
    data = request.get_json()\
    valores = np.array([data['valores']])\
    valores_esc = scaler.transform(valores)\
    pred = model.predict(valores_esc)\
    clase = int(np.argmax(pred))\
\
    recomendaciones = [\
        "\uc0\u9989  Sin Estr\'e9s: No necesita riego",\
        "\uc0\u55357 \u57314  Bajo: Monitorear",\
        "\uc0\u55357 \u57313  Medio: Considerar riego",\
        "\uc0\u55357 \u57312  Medio Alto: Programar riego pronto",\
        "\uc0\u55357 \u56628  Alto: Riego urgente",\
        "\uc0\u55357 \u57000  Severo: Riego inmediato"\
    ]\
\
    return jsonify(\{\
        "clase": clase,\
        "recomendacion": recomendaciones[clase]\
    \})\
\
if __name__ == '__main__':\
    app.run(host='0.0.0.0', port=10000)\
}