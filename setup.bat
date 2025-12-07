@echo off
echo ======================================
echo 🤖 PDF Organizer AI - Setup Automático
echo ======================================
echo.

echo 📋 Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo Por favor, instale Python 3.8 ou superior
    pause
    exit /b 1
)

echo ✅ Python OK!
echo.

echo 📦 Instalando dependências...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências!
    pause
    exit /b 1
)

echo ✅ Dependências instaladas!
echo.

echo ======================================
echo ✅ Instalação Concluída!
echo ======================================
echo.
echo Para iniciar o servidor, execute:
echo.
echo     python server.py
echo.
echo Depois acesse no navegador:
echo.
echo     http://localhost:5000
echo.
echo ======================================
pause
