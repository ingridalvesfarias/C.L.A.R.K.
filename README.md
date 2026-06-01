# ⚡ C.L.A.R.K.
### Cognitive Learning Assistant for Remarkable Knowledge

Seu assistente de IA pessoal estilo JARVIS para evoluir como desenvolvedor.

## 🚀 Como rodar

### 1. Configure o .env
Você já tem o `.env` com as chaves? Ótimo! Garanta que esteja na pasta do projeto:
```
GROQ_API_KEY=...
OPENWEATHERMAP_API_KEY=...
TAVILY_API_KEY=...
```

### 2. Inicie com um comando
```bash
./start.sh
```

Ou manualmente:
```bash
python3 -m venv venv
source venv/bin/activate       # Linux/Mac
# venv\Scripts\activate        # Windows
pip install -r requirements.txt
python app.py
```

### 3. Acesse
```
http://localhost:5000
```

## 🎙️ Recursos
- **Voz** — Clique no microfone 🎙️ e fale em português
- **TTS** — C.L.A.R.K. te responde em voz alta
- **Clima** — Pergunte sobre o tempo e ele consulta Fortaleza em tempo real
- **Busca** — Pergunte sobre novidades de tecnologia e ele pesquisa na web
- **Chat** — Tire dúvidas de código, peça revisão, ideias de projetos

## 📦 Estrutura
```
clark/
├── app.py              # Servidor Flask + lógica da IA
├── requirements.txt    # Dependências Python
├── start.sh            # Script de inicialização
├── .env                # Suas chaves (NÃO commitar!)
├── templates/
│   └── index.html      # Interface visual estilo JARVIS
└── static/
    └── clark-img.png   # Avatar do C.L.A.R.K.
```
## Imagem do Projeto:
<img src="img/imagem do projeto.png" alt="imagem do projeto">
