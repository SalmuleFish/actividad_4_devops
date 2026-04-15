import os

import boto3
from flask import Flask, jsonify, request

app = Flask(__name__)

region = "us-east-1"
dynamo = boto3.resource("dynamodb", region_name=region)
s3 = boto3.client("s3", region_name=region)

TABLE_NAME = "RastreoUnidades"
BUCKET_NAME = os.environ.get("BUCKET_EVIDENCIAS")


@app.route("/calcular-envio", methods=["POST"])
def calcular_envio():
    data = request.json
    distancia = data.get("distancia", 0)
    unidad_id = data.get("unidad_id", "UNK-001")

    costo = distancia * 1.5

    table = dynamo.Table(TABLE_NAME)
    table.put_item(Item={"UnidadID": unidad_id, "Distancia": distancia, "Costo": costo})

    file_name = f"recibo-{unidad_id}.txt"
    content = f"Envio de unidad {unidad_id}. Distancia: {distancia}km. Total: ${costo}"
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=content)

    return jsonify(
        {
            "status": "success",
            "costo": costo,
            "db": "registro_guardado",
            "s3": f"archivo_{file_name}_creado",
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "ready"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
