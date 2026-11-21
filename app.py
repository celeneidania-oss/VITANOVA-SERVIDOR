
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def inicio():
    return "¡El servidor de VITALIFE está funcionando!"

@app.route("/analizar", methods=["POST"])
def analizar():
    imagen = request.get_data()

    if not imagen:
        return jsonify({
            "error": "No se recibió ninguna imagen"
        }), 400

    tipo = request.content_type or ""

    if not tipo.startswith("image/"):
        return jsonify({
            "error": "El archivo recibido no es una imagen"
        }), 415

    return jsonify({
        "mensaje": "¡Foto recibida correctamente!",
        "estado": "recibida"
    })

if __name__ == "__main__":
    app.run()
