#!/bin/bash
echo ""
echo "  ██████╗██╗      █████╗ ██████╗ ██╗  ██╗"
echo " ██╔════╝██║     ██╔══██╗██╔══██╗██║ ██╔╝"
echo " ██║     ██║     ███████║██████╔╝█████╔╝ "
echo " ██║     ██║     ██╔══██║██╔══██╗██╔═██╗ "
echo " ╚██████╗███████╗██║  ██║██║  ██║██║  ██╗"
echo "  ╚═════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝"
echo ""
echo "  Cognitive Learning Assistant for Remarkable Knowledge"
echo ""

# Check .env
if [ ! -f ".env" ]; then
  echo "❌ ERRO: Arquivo .env não encontrado!"
  echo "   Crie o arquivo .env com as chaves: GROQ_API_KEY, OPENWEATHERMAP_API_KEY, TAVILY_API_KEY"
  exit 1
fi

# Install deps if needed
if [ ! -d "venv" ]; then
  echo "📦 Criando ambiente virtual..."
  python3 -m venv venv
fi

source venv/bin/activate

echo "📦 Verificando dependências..."
pip install -r requirements.txt -q

echo ""
echo "⚡ Iniciando C.L.A.R.K...."
echo "🌐 Acesse: http://localhost:5000"
echo ""

python app.py
