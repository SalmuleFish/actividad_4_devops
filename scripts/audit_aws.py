import boto3
import requests


def auditoria_infraestructura():
    print("--- INICIANDO AUDITORIA DE INFRAESTRUCTURA ---")
    cf = boto3.client("cloudformation", region_name="us-east-1")
    ec2 = boto3.client("ec2", region_name="us-east-1")
    s3 = boto3.client("s3", region_name="us-east-1")

    stack_name = "stack-transporte-unificado"

    stack = cf.describe_stacks(StackName=stack_name)["Stacks"][0]
    print(f"Stack: {stack_name} esta en estado {stack['StackStatus']}")

    vpcs = ec2.describe_vpcs(
        Filters=[{"Name": "tag:Name", "Values": ["VPC-Transporte"]}]
    )
    if vpcs["Vpcs"]:
        print(f"VPC Detectada: {vpcs['Vpcs'][0]['VpcId']}")

    buckets = s3.list_buckets()["Buckets"]
    transporte_bucket = [
        b["Name"] for b in buckets if "evidencias-transporte" in b["Name"]
    ]
    if transporte_bucket:
        print(f"Bucket de S3 Activo: {transporte_bucket[0]}")

    inst = ec2.describe_instances(
        Filters=[{"Name": "tag:Name", "Values": ["Servidor-Logistica"]}]
    )
    ip = inst["Reservations"][0]["Instances"][0].get("PublicIpAddress")

    if ip:
        print(f"IP del Servidor: {ip}. Probando integracion de datos...")
        url = f"http://{ip}:5000/calcular-envio"
        payload = {"distancia": 120, "unidad_id": "CAMION-77"}

        try:
            r = requests.post(url, json=payload, timeout=15)
            if r.status_code == 200:
                print("RUEBA DE INTEGRACION EXITOSA:")
                print(f"   -> Respuesta de la App: {r.json()}")
            else:
                print(f"❌ La App respondio con error {r.status_code}")
        except Exception as e:
            print(f"❌ No se pudo contactar a la App: {e}")


if __name__ == "__main__":
    auditoria_infraestructura()
