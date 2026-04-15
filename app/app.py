from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(
        {
            "status": "online",
            "empresa": "Transporte S.A. Cloud",
            "mensaje": "Sistema de logística operando en AWS Academy",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
