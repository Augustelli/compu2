#!/bin/bash

# Nombre del entorno virtual
ENV_DIR="venv"
# Verificar que pip esté instalado
if ! command -v pip &> /dev/null; then
    error "pip no está instalado. Por favor, instala pip antes de continuar."
fi
# Crear un entorno virtual
if [ -d "$ENV_DIR" ]; then
  echo "El entorno virtual '$ENV_DIR' ya existe."
else
  echo "Creando entorno virtual '$ENV_DIR'..."
  python -m venv $ENV_DIR
fi

# Activar el entorno virtual
echo "Activando entorno virtual..."
# Para Windows: source venv/Scripts/activate
# Para macOS y Linux
source $ENV_DIR/bin/activate

# Instalar dependencias desde requirements.txt
if [ -f "requirements.txt" ]; then
  echo "Instalando dependencias desde requirements.txt..."
  pip install -r requirements.txt
else
  echo "requirements.txt no encontrado. Asegúrate de que el archivo esté presente."
  exit 1
fi

# Instalar el paquete local
echo "Instalando el paquete local..."
pip install .

echo "Instalación completada."
