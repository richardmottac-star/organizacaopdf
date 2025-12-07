#!/bin/bash

echo "======================================"
echo "🤖 PDF Organizer AI - Setup Automático"
echo "======================================"
echo ""

# Check Python version
echo "📋 Verificando Python..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 não encontrado!"
    echo "Por favor, instale Python 3.8 ou superior"
    exit 1
fi

echo "✅ Python OK!"
echo ""

# Install dependencies
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências!"
    exit 1
fi

echo "✅ Dependências instaladas!"
echo ""

# Success message
echo "======================================"
echo "✅ Instalação Concluída!"
echo "======================================"
echo ""
echo "Para iniciar o servidor, execute:"
echo ""
echo "    python3 server.py"
echo ""
echo "Depois acesse no navegador:"
echo ""
echo "    http://localhost:5000"
echo ""
echo "======================================"
