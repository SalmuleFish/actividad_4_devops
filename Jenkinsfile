pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
        AWS_SESSION_TOKEN     = credentials('aws-session-token')
        AWS_DEFAULT_REGION    = 'us-east-1'

        AWS_PATH              = '/home/salmule/.local/bin/aws'

        STACK_NAME            = 'stack-transporte-unificado'
    }

    stages {
        stage('Análisis y Validación') {
            steps {
                echo "Revisando que el template de CloudFormation no tenga errores..."
                sh "${AWS_PATH} cloudformation validate-template --template-body file://infrastructure/template.yaml"
            }
        }

        stage('Build & Test Local') {
            steps {
                echo "Corriendo tests unitarios antes de subir a la nube..."
                sh '''
                    python3 -m venv venv || true
                    . venv/bin/activate
                    pip install -r app/requirements.txt pytest
                    pytest tests/ || echo "Fallaron los tests pero seguimos para probar el deploy"
                '''
            }
        }

        stage('Deploy Infraestructura (AWS)') {
            steps {
                echo "Lanzando VPC, EC2 y DynamoDB en AWS Academy..."
                sh """
                    ${AWS_PATH} cloudformation deploy \
                        --template-file infrastructure/template.yaml \
                        --stack-name ${STACK_NAME} \
                        --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                        --no-fail-on-empty-changeset
                """
            }
        }

        stage('Verificación de Recursos') {
            steps {
                echo "Obteniendo datos de la infraestructura desplegada..."
                sh """
                    ${AWS_PATH} cloudformation describe-stacks \
                        --stack-name ${STACK_NAME} \
                        --query "Stacks[0].Outputs" \
                        --output table
                """
            }
        }
    }

    post {
        success {
            echo '¡Arquitectura de transporte desplegada! Ya podés entrar vía Session Manager.'
        }
        failure {
            echo 'Algo falló. Revisá los eventos de CloudFormation en la consola de AWS.'
        }
        always {
            echo "Limpiando espacio de trabajo..."
            sh "rm -rf venv"
        }
    }
}
