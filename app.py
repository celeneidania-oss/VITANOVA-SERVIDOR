
import os
import json
import base64
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

@app.route("/")
def inicio():
    return "¡El servidor de VITANOVA está funcionando!"

@app.route("/analizar", methods=["POST"])
def analizar():
    imagen = request.get_data()

    if not imagen:
        return jsonify({"error": "No se recibió ninguna imagen"}), 400

    tipo = request.headers.get("Content-Type", "")
    if "image/png" in tipo:
        formato = "image/png"
    elif "image/webp" in tipo:
        formato = "image/webp"
    else:
        formato = "image/jpeg"

    foto = base64.b64encode(imagen).decode("utf-8")
    imagen_url = f"data:{formato};base64,{foto}"

    try:
        cliente = OpenAI()

        respuesta = cliente.responses.create(
            model="gpt-5.5",
            input=[{
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Observa esta comida. Devuelve únicamente un "
                            "objeto JSON con las claves alimento, calorias, "
                            "carbohidratos, proteinas y grasas. Estima los "
                            "nutrientes de la porción visible. Usa números "
                            "para los nutrientes y aclara que son aproximados."
                        )
                    },
                    {
                        "type": "input_image",
                        "image_url": imagen_url
                    }
                ]
            }]
        )

        datos = json.loads(respuesta.output_text)
        return jsonify(datos)

    except Exception:
        app.logger.exception("Error al analizar la imagen")
        return jsonify({
            "error": "No se pudo analizar la imagen"
        }), 500
