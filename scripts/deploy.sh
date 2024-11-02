#!/bin/bash
set -e

# Activar entorno virtual (descomenta la línea si tenés un entorno virtual configurado)
# source .venv/bin/activate

if ! aws sts get-caller-identity &> /dev/null; then
    echo "Error: AWS CLI no está configurado correctamente. Ejecuta 'aws configure'"
    exit 1
fi

pip install -r requirements.txt

pip install aws-sam-cli

sam validate

sam build

sam deploy \
    --stack-name :YOURSTACKNAME: \
    --capabilities CAPABILITY_IAM \
    --region us-east-2 \
    --confirm-changeset

echo "Despliegue completado exitosamente"
