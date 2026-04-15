# Plan de Migracion Cloud - Empresa de Transporte S.A.

Este repositorio contiene la solucion tecnica para la migracion de la infraestructura local de una empresa de transporte hacia Amazon Web Services (AWS), utilizando metodologias DevOps y herramientas de Automatizacion.

## Descripcion del Proyecto
El objetivo es migrar sistemas de informacion alojados en servidores locales hacia una arquitectura escalable, segura y de alta disponibilidad en AWS Academy (Learner Lab). La solucion incluye el despliegue de redes, computo, bases de datos y almacenamiento de forma automatizada.

## Arquitectura de la Solucion
La infraestructura se despliega mediante CloudFormation e incluye:
- VPC con segmentacion de subredes publicas.
- Instancia EC2 (t3.micro) para el servidor de logistica.
- Tabla DynamoDB para el rastreo de unidades en tiempo real.
- Bucket S3 para el almacenamiento de evidencias y remitos.
- Acceso seguro mediante AWS Systems Manager (SSM), eliminando la necesidad de llaves SSH.

## Componentes del Repositorio
- /infrastructure: Contiene el template de CloudFormation para el despliegue de recursos.
- /app: Codigo fuente de la aplicacion Flask contenedorizada con Docker.
- /scripts: Scripts de Python para auditoria de infraestructura y pruebas de conectividad.
- Jenkinsfile: Pipeline de CI/CD que coordina la validacion, el despliegue y las pruebas.

## Requisitos Previos
1. Cuenta de AWS Academy (Learner Lab) activa.
2. Credenciales de AWS configuradas en Jenkins (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN).
3. Jenkins instalado con los plugins de Pipeline y Docker.

## Instrucciones de Despliegue
1. Clonar este repositorio en su servidor de Jenkins.
2. Asegurarse de que el archivo infrastructure/template.yaml contenga el nombre correcto del LabRole.
3. Ejecutar el Pipeline desde la interfaz de Jenkins.
4. Una vez finalizado el despliegue, el script de auditoria verificara automaticamente la conectividad y la persistencia de datos en S3 y DynamoDB.

## Pruebas de Integridad
El sistema realiza las siguientes validaciones post-despliegue:
- Verificacion de estado del Stack en CloudFormation.
- Comprobacion de visibilidad de la IP publica del servidor.
- Prueba funcional de calculo de costos de envio con guardado en Base de Datos y Almacenamiento.

## Seguridad
- Implementacion de politicas de minimo privilegio mediante LabRole.
- Uso de MFA para accesos administrativos (configuracion teorica documentada).
- Monitoreo activo de recursos mediante Amazon CloudWatch.
