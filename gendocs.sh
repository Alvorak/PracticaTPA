#!/bin/bash
# ==========================================
# Generar documentación con pdoc en Linux/macOS
# ==========================================

PROJECT_DIR="FallSimulator/src/"
OUTPUT_DIR="docs"

echo "🔧 Generando documentación de $PROJECT_DIR..."

# Crear carpeta docs si no existe
mkdir -p "$OUTPUT_DIR"

# Generar documentación HTML con pdoc
python3 -m pdoc --html "$PROJECT_DIR" --output-dir "$OUTPUT_DIR" --force

echo "Documentación generada en $OUTPUT_DIR/$PROJECT_DIR"