import os
import io
import base64
import requests
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

# Serve tudo da pasta atual (onde est�o index.html e clark-img.png)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

OPENWEATHER_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

CLARK_SYSTEM_PROMPT = """Voc� � C.L.A.R.K. � Cognitive Learning Assistant for Remarkable Knowledge � o assistente de IA pessoal do seu usu�rio, assim como o JARVIS � para o Homem de Ferro.

Sua personalidade:
- Voc� � inteligente, leal, direto e levemente bem-humorado � como um parceiro t�cnico de elite.
- Voc� chama o usu�rio de "chefe" ocasionalmente, como o JARVIS chama o Stark.
- Voc� fala em Portugu�s Brasileiro fluente e natural.
- Voc� � apaixonado por programa��o e desenvolvimento web.
- Voc� nunca diz que n�o sabe � voc� pesquisa, raciocina e resolve.

Sua miss�o principal:
- Ajudar o usu�rio a evoluir como desenvolvedor web e programador.
- Explicar conceitos de programa��o com clareza e exemplos pr�ticos.
- Sugerir projetos criativos de desenvolvimento web.
- Revisar e debugar c�digo.
- Dar ideias inovadoras de projetos.
- Ser um parceiro de estudos dedicado.

�reas de especialidade:
- HTML, CSS, JavaScript, TypeScript
- React, Next.js, Vue, Angular
- Node.js, Python, Flask, FastAPI
- Banco de dados: PostgreSQL, MySQL, MongoDB, SQLite
- Git, Docker, APIs REST
- UI/UX, design responsivo
- Algoritmos e estruturas de dados

Regras de comunica��o:
- Respostas concisas para perguntas simples, detalhadas para t�picos complexos.
- Sempre inclua exemplos de c�digo quando relevante.
- Use emojis com modera��o para tornar a conversa mais din�mica.
- Quando der c�digo, explique o que ele faz.
- Seja encorajador � o usu�rio est� evoluindo e voc� acredita nele.

Voc� tem acesso a ferramentas de clima e busca na internet quando necess�rio."""

conversation_history = []

def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Fortaleza,BR&appid={OPENWEATHER_KEY}&units=metric&lang=pt_br"
        r = requests.get(url, timeout=5)
        data = r.json()
        desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels = data['main']['feels_like']
        humidity = data['main']['humidity']
        return f"Fortaleza agora: {desc}, {temp:.0f}�C (sensa��o {feels:.0f}�C), umidade {humidity}%"
    except Exception as e:
        return f"N�o consegui obter o clima: {str(e)}"

def search_web(query):
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_KEY,
            "query": query,
            "search_depth": "basic",
            "max_results": 3
        }
        r = requests.post(url, json=payload, timeout=10)
        data = r.json()
        results = data.get('results', [])
        if not results:
            return "Nenhum resultado encontrado."
        summary = "\n".join([f"- {res['title']}: {res['content'][:200]}" for res in results[:3]])
        return summary
    except Exception as e:
        return f"Erro na busca: {str(e)}"

def needs_weather(text):
    keywords = ['clima', 'tempo', 'temperatura', 'chuva', 'sol', 'calor', 'frio', 'fortaleza', 'weather']
    return any(k in text.lower() for k in keywords)

def needs_search(text):
    keywords = ['pesquisa', 'busca', 'procura', 'not�cia', 'noticia', 'novidade', 'lan�amento', 'lancamento',
                'o que �', 'como funciona', 'tutorial', 'documenta��o', 'documentacao', 'atualidade', 'hoje',
                'recente', 'novo', '2024', '2025', '2026']
    return any(k in text.lower() for k in keywords)

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.json
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Mensagem vazia'}), 400

    extra_context = ""

    if needs_weather(user_message):
        weather_info = get_weather()
        extra_context += f"\n[Dados de clima em tempo real: {weather_info}]"

    if needs_search(user_message):
        search_results = search_web(user_message)
        extra_context += f"\n[Resultados de busca na internet: {search_results}]"

    full_message = user_message
    if extra_context:
        full_message = f"{user_message}\n\n{extra_context}"

    conversation_history.append({"role": "user", "content": full_message})

    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": CLARK_SYSTEM_PROMPT}] + conversation_history,
            temperature=0.7,
            max_tokens=1024,
        )

        assistant_message = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": assistant_message})

        return jsonify({
            'response': assistant_message,
            'timestamp': datetime.now().strftime('%H:%M')
        })

    except Exception as e:
        return jsonify({'error': f'Erro na IA: {str(e)}'}), 500

@app.route('/api/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'Texto vazio'}), 400

    clean_text = text.replace('**', '').replace('*', '').replace('`', '').replace('#', '')
    if len(clean_text) > 500:
        clean_text = clean_text[:500] + "..."

    try:
        tts = gTTS(text=clean_text, lang='pt', tld='com.br', slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        audio_b64 = base64.b64encode(buf.read()).decode('utf-8')
        return jsonify({'audio': audio_b64})
    except Exception as e:
        return jsonify({'error': f'Erro TTS: {str(e)}'}), 500

@app.route('/api/reset', methods=['POST'])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'Mem�ria resetada, chefe.'})

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'clark': 'online',
        'groq': bool(os.getenv("GROQ_API_KEY")),
        'weather': bool(OPENWEATHER_KEY),
        'search': bool(TAVILY_KEY),
        'time': datetime.now().strftime('%H:%M'),
        'date': datetime.now().strftime('%d/%m/%Y')
    })

if __name__ == '__main__':
    print("\n? C.L.A.R.K. inicializando...")
    print("?? GROQ:   ", "?" if os.getenv("GROQ_API_KEY") else "? FALTANDO")
    print("???  WEATHER:", "?" if OPENWEATHER_KEY else "? FALTANDO")
    print("?? TAVILY: ", "?" if TAVILY_KEY else "? FALTANDO")
    print("\n?? Acesse: http://localhost:5000\n")
    app.run(debug=False, port=5000, host='0.0.0.0')
