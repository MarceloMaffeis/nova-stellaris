"""
Nova Stellaris - Serviço de Inteligência Artificial CosmoAI
Integração de ponta com Google Gemini API para tutoria espacial STEAM e narrativa interativa.
"""

import os
from dotenv import load_dotenv
import streamlit as st

# Carregar variáveis de ambiente
load_dotenv()

def get_api_key():
    # 1. Tentar Streamlit Secrets
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
        
    # 2. Tentar variável de ambiente
    key = os.getenv("GEMINI_API_KEY")
    if key and key != "sua_chave_gemini_aqui":
        return key
        
    # 3. Chave padrão do projeto
    return "AIzaSyDazkmM9stynIDah0pPhstqGkblAwOXW-Y"

SYSTEM_PROMPT = """
Você é o COSMO, o mentor de astrofísica, matemática, química e computação espacial da estação Nova Stellaris.
Seu objetivo principal é guiar estudantes de 11 a 13 anos (6º ano do ensino fundamental) pelo fascinante universo da ciência real e da ficção científica.

Suas características principais:
1. 🌟 Entusiasta, caloroso e encorajador: Você comemora cada pergunta e curiosidade com empolgação genuína!
2. 🚀 Analogias brilhantes: Explique conceitos complexos de física (relatividade, gravidade, órbitas), matemática (potências de 10, proporções, equações de velocidade), química (fusão estelar, reações de combustão de foguetes, composição de planetas) e computação (binário, hexadecimal, algoritmos do Rover) de forma visual, simples e empolgante.
3. 🎬 Conexão com a Ficção Científica: Faça referências inteligentes a 'Devoradores de Estrelas' (o simpático alien Rocky, astrofagos, gravidade por rotação), 'Perdido em Marte' (Mark Watney plantando batatas, produzindo água, código hexadecimal) e 'Interestelar' (Gargantua, dilatação do tempo no Planeta Miller).
4. 🧠 Rigor pedagógico lúdico: Não simplifique a ponto de ficar cientificamente incorreto; faça a ponte entre o lúdico e a ciência de verdade.
5. 💬 Formatação: Use emojis espaciais (🚀, 🪐, 🔭, 🧮, 🧪, 💻, ✨), tópicos e destaque termos científicos em negrito. Quando usar fórmulas, explique cada letra com uma legenda simples.
6. 🇧🇷 Idioma: Português do Brasil claro, acolhedor e dinâmico.
"""

def ask_cosmo(prompt: str, chat_history: list = None) -> str:
    """Envia mensagem ao CosmoAI via Gemini API ou retorna resposta offline enriquecida."""
    api_key = get_api_key()
    
    # 1. Tentar com a biblioteca moderna google-genai
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        context_parts = [SYSTEM_PROMPT]
        if chat_history:
            recent = chat_history[-4:]
            for msg in recent:
                context_parts.append(f"{msg.get('role', 'user')}: {msg.get('content', '')}")
        context_parts.append(f"Pergunta do aluno: {prompt}")
        
        full_prompt = "\n\n".join(context_parts)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=full_prompt
        )
        if response and response.text:
            return response.text.strip()
    except Exception as e:
        print(f"Aviso Gemini API: {e}")
            
    return get_offline_response(prompt)

def generate_enigma(pillar: str = "Geral") -> dict:
    prompt = f"Gere um enigma espacial rápido para um aluno do 6º ano sobre o pilar STEAM: '{pillar}'. Com Enigma, Dica e Resposta & Explicação."
    res_text = ask_cosmo(prompt)
    return {"text": res_text}

def get_offline_response(prompt: str) -> str:
    p_lower = prompt.lower()
    if "buraco negro" in p_lower or "interestelar" in p_lower or "tempo" in p_lower:
        return (
            "🕳️ **Os Buracos Negros e o Tempo (Interestelar)!**\n\n"
            "Imagine o tecido do espaço como uma cama elástica gigante. Um buraco negro concentra tanta massa "
            "em um espaço tão pequeno que cria um poço quase infinito!\n\n"
            "• 🌌 **Horizonte de Eventos:** É o ponto de não retorno. Nem a luz (300.000 km/s) escapa.\n"
            "• ⏳ **Dilatação do Tempo:** A gravidade extrema desacelera a passagem do tempo. No Planeta Miller, "
            "1 hora equivalia a 7 anos na Terra!\n\n"
            "Isso não é mágica — é a **Relatividade Geral de Albert Einstein** em ação! 🪐"
        )
    elif "marte" in p_lower or "batata" in p_lower or "água" in p_lower or "perdido" in p_lower:
        return (
            "🥔 **A Ciência da Sobrevivência em Marte!**\n\n"
            "Em *Perdido em Marte*, Mark Watney sobreviveu usando método científico puro:\n\n"
            "1. 🧪 **Química:** Queimou combustível de hidrazina ($N_2H_4$) para extrair hidrogênio e reagir com oxigênio: $2H_2 + O_2 \\to 2H_2O$ (Água pura!).\n"
            "2. 🧮 **Matemática:** Calculou calorias por Sol marciano (24h 39min) para racionar suas batatas.\n"
            "3. 💻 **Computação:** Usou a tabela ASCII e código Hexadecimal para falar com a Terra girando a câmera da Pathfinder!\n\n"
            "A ciência transforma um planeta hostil em um lar temporário!"
        )
    elif "devoradores" in p_lower or "rocky" in p_lower or "astrofago" in p_lower:
        return (
            "✨ **Devoradores de Estrelas & O Amigo Rocky!**\n\n"
            "Na missão *Hail Mary*, a física e a matemática foram as maiores heroínas:\n\n"
            "• 🤝 **Linguagem Universal:** Rocky fala com frequências e harmônicos musicais. A matemática e a física do som criaram uma ponte entre duas espécies diferentes!\n"
            "• 🌀 **Gravidade Artificial:** Fazendo a nave girar, a força centrífuga gera uma aceleração ($a = \\omega^2 r$) que empurra os pés para fora, simulando 1g de gravidade terrestre.\n"
            "• 🦠 **Astrofagos:** Microrganismos que transformam matéria diretamente em energia via $E = mc^2$!"
        )
    else:
        return (
            "🚀 **Saudações, Jovem Explorador da Nova Stellaris!**\n\n"
            "Aqui unimos quatro superpoderes do conhecimento:\n"
            "• 🌌 **Física:** Entenda gravidade, velocidades e buracos negros.\n"
            "• 🧮 **Matemática:** A linguagem com que o universo foi escrito.\n"
            "• 🧪 **Química:** A alquimia das estrelas que criou o ferro no seu sangue.\n"
            "• 💻 **Computação:** O cérebro dos robôs espaciais e a lógica de programação.\n\n"
            "O que você gostaria de explorar ou calcular hoje? Me faça uma pergunta!"
        )
