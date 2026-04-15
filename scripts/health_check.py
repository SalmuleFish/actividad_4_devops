import sys

import boto3
import requests


def get_instance_ip(stack_name):
    """Obtiene la IP publica de la instancia desde los Outputs de CloudFormation."""
    cf = boto3.client("cloudformation", region_name="us-east-1")
    try:
        response = cf.describe_stacks(StackName=stack_name)
        outputs = response["Stacks"][0].get("Outputs", [])

        instance_id = next(
            (o["OutputValue"] for o in outputs if o["OutputKey"] == "InstanceId"), None
        )

        if not instance_id:
            print("❌ No se encontro el InstanceId en los outputs del Stack")
            return None

        ec2 = boto3.client("ec2", region_name="us-east-1")
        inst = ec2.describe_instances(InstanceIds=[instance_id])
        ip = inst["Reservations"][0]["Instances"][0].get("PublicIpAddress")
        return ip

    except Exception as e:
        print(f"❌ Error al conectar con AWS: {e}")
        return None


def check_service(ip, port=80):
    """Prueba si el servicio web responde en la IP indicada."""
    url = f"http://{ip}:{port}"
    print(f"Verificando conectividad con {url}...")
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            print(f"Servicio funcionando, codigo: {r.status_code}")
            return True
        else:
            print(f"El servidor respondio con codigo: {r.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ El servidor no responde")
        return False


if __name__ == "__main__":
    STACK = "stack-transporte-unificado"

    public_ip = get_instance_ip(STACK)

    if public_ip:
        print(f"IP Publica detectada: {public_ip}")
        success = check_service(public_ip, port=80)
        if not success:
            print("Esperar 2 min a que UserData termine de instalar todo")
    else:
        print("No se pudo realizar el health check")
        sys.exit(1)
