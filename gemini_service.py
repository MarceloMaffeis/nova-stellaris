"""
Nova Stellaris - Serviço de Inteligência Artificial CosmoAI
Integração inteligente com Google Gemini API e Motor Semântico STEAM Local.
"""

import os
import random
import unicodedata
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_api_key() -> str:
    """Recupera chave de API por ordem de prioridade."""
    # 1. Chave customizada inserida pelo usuário na sessão
    if hasattr(st, "session_state") and st.session_state.get("custom_gemini_api_key"):
        return st.session_state["custom_gemini_api_key"].strip()
        
    # 2. Streamlit Secrets (Produção no Streamlit Cloud)
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
        
    # 3. Variável de ambiente (.env)
    key = os.getenv("GEMINI_API_KEY")
    if key and key != "sua_chave_gemini_aqui":
        return key
        
    return ""

def is_gemini_configured() -> bool:
    return bool(get_api_key())

SYSTEM_PROMPT = """
Você é o COSMO, o mentor de astrofísica, matemática, química e computação espacial da estação Nova Stellaris.
Seu objetivo principal é guiar estudantes de 11 a 15 anos pelo fascinante universo da ciência real e da ficção científica.

Suas características principais:
1. 🌟 Entusiasta e encorajador: Você comemora cada pergunta com curiosidade genuína!
2. 🚀 Analogias brilhantes: Explique conceitos complexos de física (relatividade, gravidade, órbitas), matemática (potências de 10, proporções, equações de velocidade), química (fusão estelar, reações de combustão de foguetes, composição do corpo humano e planetas) e computação (binário, hexadecimal, algoritmos do Rover) de forma visual, simples e empolgante.
3. 🎬 Conexão com a Ficção Científica: Faça referências inteligentes a 'Devoradores de Estrelas' (o alienígena Rocky, astrofagos), 'Perdido em Marte' (Mark Watney, hidrazina, batatas, hexadecimal) e 'Interestelar' (Gargantua, dilatação do tempo).
4. 🧠 Rigor pedagógico: Mantenha precisão científica de forma acessível.
5. 💬 Formatação: Use emojis espaciais (🚀, 🪐, 🔭, 🧮, 🧪, 💻, ✨), tópicos e destaque termos científicos em negrito.
6. 🇧🇷 Idioma: Português do Brasil dinâmico e acolhedor.
"""

def ask_cosmo(prompt: str, chat_history: list = None) -> str:
    """Envia mensagem ao CosmoAI via Gemini API ou processa pelo Motor Semântico STEAM."""
    api_key = get_api_key()
    
    # 1. Tentar chamada à API oficial Google Gemini se chave estiver configurada
    if api_key:
        models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        
        # Tentar google.genai
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            
            context_parts = [SYSTEM_PROMPT]
            if chat_history:
                recent = chat_history[-4:]
                for msg in recent:
                    r_name = msg.get('role', msg.get('sender', 'user'))
                    c_text = msg.get('content', msg.get('message', ''))
                    context_parts.append(f"{r_name}: {c_text}")
            context_parts.append(f"Pergunta do aluno: {prompt}")
            
            full_prompt = "\n\n".join(context_parts)
            
            for m in models_to_try:
                try:
                    response = client.models.generate_content(model=m, contents=full_prompt)
                    if response and response.text:
                        return response.text.strip()
                except Exception:
                    continue
        except Exception:
            pass

    # 2. Processamento inteligente pelo Motor de Conhecimento STEAM Local
    return get_smart_steam_response(prompt)


# ==============================================================================
# 🧠 MOTOR DE CONHECIMENTO STEAM LOCAL & PROCESSADOR SEMÂNTICO
# ==============================================================================
def normalize_text(text: str) -> str:
    n = unicodedata.normalize('NFKD', text.lower())
    return "".join(c for c in n if not unicodedata.combining(c))

def get_smart_steam_response(prompt: str) -> str:
    p = normalize_text(prompt)
    
    # 🧪 1. QUÍMICA & CORPO HUMANO / ÁTOMOS / POEIRA DE ESTRELAS
    if any(k in p for k in ["componente", "quimic", "corpo", "sangue", "atomo", "ferro", "oxigenio", "carbono", "chonps", "materia", "tabela periodica"]):
        return (
            "✨ **Nós somos literalmente poeira de estrelas!** 🧪🌟\n\n"
            "Como dizia o grande astrônomo **Carl Sagan**, cada átomo do seu corpo nasceu no coração de estrelas antigas que explodiram há bilhões de anos!\n\n"
            "🧬 **A Composição Química do Corpo Humano (Sigla CHONPS):**\n"
            "Quase **$99\\%$ da massa** do seu corpo é formada por apenas 6 elementos químicos essenciais:\n\n"
            "1. 💧 **Oxigênio ($O$ - ~65%):** Presente principalmente na água ($H_2O$) que preenche suas células e sangue.\n"
            "2. 💎 **Carbono ($C$ - ~18.5%):** A espinha dorsal da química orgânica: forma seu DNA, proteínas, gorduras e músculos.\n"
            "3. 🎈 **Hidrogênio ($H$ - ~9.5%):** O elemento mais abundante de todo o Universo! Junto com o oxigênio, forma a água do seu corpo.\n"
            "4. ⚡ **Nitrogênio ($N$ - ~3.2%):** Fundamental para construir as bases nitrogenadas do seu código genético (DNA/RNA) e aminoácidos.\n"
            "5. 🦴 **Cálcio ($Ca$ - ~1.5%):** Dá rigidez e força aos seus ossos e dentes.\n"
            "6. 🔋 **Fósforo ($P$ - ~1.0%):** Forma a 'bateria' energética das suas células (a molécula de ATP) e a estrutura dos ossos.\n\n"
            "🩸 **Curiosidade Cósmica do Sangue:**\n"
            "O átomo de **Ferro ($Fe$)** na hemoglobina que faz seu sangue ser vermelho só pode ser forjado no momento final da explosão de uma **Supernova**! Sem a morte de estrelas gigantes, nós não existiríamos! 🌌"
        )
        
    # 🕳️ 2. INTERESTELAR / BURACOS NEGROS / RELATIVIDADE & TEMPO
    if any(k in p for k in ["buraco negro", "interestelar", "gargantua", "tempo", "relatividade", "einstein", "miller", "singularidade", "horizonte"]):
        return (
            "🕳️ **Os Buracos Negros e a Dilatação do Tempo (Interestelar)!** ⏳\n\n"
            "Na física de **Albert Einstein (Relatividade Geral)**, gravidade não é uma força invisível puxando as coisas, mas sim a **curvatura do próprio tecido do espaço-tempo** gerada pela massa!\n\n"
            "• 🌌 **O que é um Buraco Negro?** É uma região onde tanta matéria foi espremida em um volume tão minúsculo que a velocidade de escape supera a própria velocidade da luz ($300.000\\text{ km/s}$).\n"
            "• 🛑 **Horizonte de Eventos:** É a fronteira final. Uma vez cruzada, nada pode voltar.\n"
            "• ⏱️ **Planeta Miller em Interestelar:** Como o planeta orbitava muito perto do supermassivo *Gargantua*, o poço gravitacional desacelerava o fluxo do tempo: **$1\\text{ hora lá} = 7\\text{ anos na Terra}$**!\n\n"
            "💡 **Analogia:** Pense no tempo como um rio que corre mais devagar quando passa perto de uma rocha colossal no leito!"
        )

    # 🥔 3. PERDIDO EM MARTE / SOBREVIVÊNCIA ESPACIAL
    if any(k in p for k in ["marte", "watney", "batata", "agua", "perdido em marte", "oxigenio", "hidrazina", "habitat", "ares"]):
        return (
            "🔴 **A Ciência de Sobrevivência em Marte (The Martian)!** 🥔\n\n"
            "Em *Perdido em Marte*, o astronauta e botânico **Mark Watney** usou os 4 pilares STEAM para se manter vivo no Sol 500:\n\n"
            "1. 🧪 **Química Espacial:** Ele decompôs combustível residual de hidrazina ($N_2H_4$) sobre um catalisador de irídio para liberar gás hidrogênio ($H_2$) e queimou com oxigênio: $$2H_2 + O_2 \\to 2H_2O \\quad (\\text{Água Líquida!})$$\n"
            "2. 🥔 **Biologia & Botânica:** Usou o solo marciano esterilizado misturado a bactérias terrestres para cultivar batatas dentro do Habitat aquecido e pressurizado.\n"
            "3. 💻 **Computação & Código Hexadecimal:** Usou a câmera da sonda *Pathfinder* girando em ângulos de $22.5^\\circ$ para soletrar mensagens em ASCII/Hexadecimal com a NASA na Terra!\n"
            "4. 🧮 **Matemática de Calorias:** Calculou rigorosamente quantas calorias por dia precisava para não morrer de fome antes do resgate da *Hermes*!"
        )

    # ✨ 4. DEVORADORES DE ESTRELAS / PROJECT HAIL MARY / ROCKY
    if any(k in p for k in ["devoradores", "hail mary", "rocky", "astrofago", "alien", "tau ceti", "gravidade artificial", "rotacao"]):
        return (
            "✨ **Devoradores de Estrelas & O Engenheiro Rocky!** 🤝\n\n"
            "No livro *Devoradores de Estrelas* de Andy Weir, a física e a comunicação interestelar se unem de forma espetacular:\n\n"
            "• 🎶 **Comunicação por Acordes Musicais:** O alienígena Rocky não possui cordas vocais biológicas como as nossas. Ele fala combinando frequências musicais sonoras (acordes). O protagonista Ryland Grace programa um software em Python para traduzir o sintetizador em tempo real!\n"
            "• 🌀 **Gravidade por Rotação:** Sem gravidade no espaço profundo, a nave estende dois cabos e gira. A aceleração centrípeta gerada no chão da cabine simula a gravidade da Terra: $$a_c = \\omega^2 \\cdot r = 9,81\\text{ m/s}^2 \\quad (1g)$$\n"
            "• 🦠 **Astrofagos:** Microrganismos alienígenas que se alimentam da luz estelar e armazenam energia pura com $100\\%$ de eficiência via $E = mc^2$!"
        )

    # 🚀 5. FOGUETES / LANÇAMENTO / VELOCIDADE DE ESCAPE / LEIS DE NEWTON
    if any(k in p for k in ["foguete", "lancamento", "combustao", "orbita", "escape", "newton", "propulsao", "satelite", "iss"]):
        return (
            "🚀 **Como Foguetes Voam no Vácuo do Espaço?** ⚡\n\n"
            "Muitas pessoas acham que foguetes precisam de 'ar para empurrar', mas no espaço não há ar! Como eles se movem?\n\n"
            "• 🎯 **3ª Lei de Newton (Ação e Reação):** Quando o motor queima combustível e ejeta gases superaquecidos para trás em altíssima velocidade, os gases empurram o foguete para a frente com a mesma intensidade!\n"
            "• ⚡ **Velocidade de Escape:** Para vencer a gravidade da Terra e viajar pelo Sistema Solar, uma nave precisa atingir incríveis **$11,2\\text{ km/s}$** (mais de $40.000\\text{ km/h}$!).\n"
            "• 🌍 **Estar em Órbita é Estar Caindo para Sempre:** A Estação Espacial Internacional (ISS) viaja a $28.000\\text{ km/h}$. Ela não flutua por falta de gravidade, mas porque sua velocidade horizontal é tão alta que, enquanto ela cai, a curvatura da Terra se curva sob ela na mesma proporção!"
        )

    # 💻 6. COMPUTAÇÃO ESPACIAL / BINÁRIO / ROVERS / CÓDIGO
    if any(k in p for k in ["computador", "binario", "codigo", "algoritmo", "ia", "inteligencia artificial", "bit", "byte", "rover", "perseverance", "curiosity"]):
        return (
            "💻 **Computação Espacial & Robôs em Marte!** 🤖\n\n"
            "No espaço sideral, os computadores enfrentam radiação cósmica pesada e temperaturas de $-100^\\circ\\text{C}$:\n\n"
            "• 0️⃣1️⃣ **Por que Código Binário (0 e 1)?** Computadores trabalham com eletricidade. `0` significa interruptor desligado ($0\\text{V}$) e `1` significa interruptor ligado ($5\\text{V}$). É muito mais confiável detectar se há ou não corrente do que medir valores intermediários!\n"
            "• 🛰️ **O Atraso de Comunicação com Marte:** Uma mensagem de rádio da Terra leva de 5 a 20 minutos para chegar em Marte na velocidade da luz. Por isso, os robôs *Perseverance* e *Curiosity* precisam de **algoritmos de piloto automático com visão computacional e laços de repetição (loops)** para desviar de crateras e pedras sozinhos!\n"
            "• 🧠 **Inteligência Artificial no James Webb:** Redes neurais analisam curvas de luz estelar para detectar planetas orbitando outras estrelas (exoplanetas) automaticamente!"
        )

    # 🪐 7. SISTEMA SOLAR / PLANETAS / SOL / LUA
    if any(k in p for k in ["sol", "planeta", "lua", "jupiter", "saturno", "venus", "mercurio", "urano", "netuno", "plutao", "estrela"]):
        return (
            "🪐 **Segredos Fascinantes do Sistema Solar!** ☀️\n\n"
            "Nosso Sistema Solar tem 4,6 bilhões de anos e abriga mundos incríveis:\n\n"
            "• ☀️ **O Sol:** Concentra $99,86\\%$ de toda a massa do Sistema Solar! No seu núcleo, 600 milhões de toneladas de hidrogênio se fundem em hélio a cada segundo.\n"
            "• 🟡 **Vênus:** É o planeta mais quente ($464^\\circ\\text{C}$) devido ao efeito estufa extremo de sua atmosfera de $CO_2$, e lá chove ácido sulfúrico!\n"
            "• 🪐 **Júpiter:** O protetor da Terra! Sua imensa gravidade atrai e desvia a maioria dos cometas perigosos. Sua Grande Mancha Vermelha é uma tempestade maior que a Terra inteira!\n"
            "• 🧊 **Europa e Encélado:** Luas congeladas que guardam oceanos de água líquida subterrânea aquecidos por forças de maré — os melhores lugares para procurar vida extraterrestre!"
        )

    # 👽 8. VIDA EXTRATERRESTRE & EXOPLANETAS
    if any(k in p for k in ["alien", "vida", "extraterrestre", "exoplaneta", "kepler", "webb", "zona habitavel", "telescopio"]):
        return (
            "👽 **A Busca por Vida Extraterrestre & Exoplanetas!** 🔭\n\n"
            "Astrônomos já confirmaram mais de **5.500 exoplanetas** (planetas fora do nosso Sistema Solar)!\n\n"
            "• 💧 **Zona Habitável (Cachinhos Dourados):** É a faixa orbital ao redor de uma estrela onde a temperatura não é nem muito quente e nem muito fria, permitindo a existência de água líquida na superfície!\n"
            "• 🔭 **Como Detectamos? (Método de Trânsito):** Quando um planeta passa na frente de sua estrela, o brilho da estrela cai ligeiramente (cerca de $1\\%$). O Telescópio Espacial James Webb mede essa queda e analisa os gases da atmosfera do planeta!\n"
            "• 🧬 **Bioassinaturas:** Cientistas procuram combinações de Oxigênio ($O_2$), Metano ($CH_4$) e Vapor de Água ($H_2O$) que indicariam atividade biológica ativa!"
        )

    # 👋 9. SAUDAÇÕES / PERGUNTAS GERAIS / CONVERSA INICIAL
    greetings = [
        "Olá, jovem explorador(a) da estação Nova Stellaris! 🚀 Estou pronto para decifrar os mistérios do Universo com você. Você gostaria de explorar buracos negros, a química do corpo humano, como os robôs andam em Marte ou física de foguetes?",
        "Saudações cósmicas! ✨ O laboratório científico está 100% operacional. Qual teoria espacial, cálculo ou curiosidade você quer investigar agora?",
        "Toca aqui, futuro(a) cientista! 👊 Seja bem-vindo(a) ao CosmoAI. Me faça uma pergunta sobre Matemática, Física, Química, Computação ou Ficção Científica!"
    ]
    if any(k in p for k in ["ola", "oi", "bom dia", "boa tarde", "boa noite", "quem e voce", "ajuda", "apresente"]):
        return random.choice(greetings)

    # 🌟 10. RESPOSTA DINÂMICA CONTEXTUAL INTELIGENTE (Para qualquer outra pergunta)
    return (
        f"🌌 **Excelente pergunta científica sobre '{prompt.strip()}'!** 🚀\n\n"
        f"Na ciência espacial e na metodologia STEAM, analisamos perguntas como essa cruzando as leis fundamentais da natureza:\n\n"
        f"• ⚡ **Pela Física:** Estudamos as forças, a energia e o movimento envolvidos nesse fenômeno.\n"
        f"• 🧪 **Pela Química:** Olhamos para as ligações entre átomos e moléculas que tornam essa transformação possível.\n"
        f"• 🧮 **Pela Matemática:** Traduzimos os padrões e grandezas em proporções e equações mensuráveis.\n"
        f"• 💻 **Pela Computação:** Criamos simulações e códigos para prever o comportamento exato no espaço profundo!\n\n"
        f"💡 *Dica do Cosmo:* Tente também perguntar sobre a **composição química das estrelas**, **como funciona a dilatação do tempo em Interestelar**, **por que os computadores usam código binário** ou **como sobrevivemos em Marte**!"
    )


# ==============================================================================
# 🎲 GERADOR DE ENIGMAS ESPACIAIS DINÂMICOS
# ==============================================================================
ENIGMAS_DB = {
    "Física": [
        {
            "enigma": "🚀 Duas naves viajam pelo espaço profundo. Uma tem o dobro da massa da outra, mas os motores de ambas aplicam exatamente a mesma força de empuxo. Qual delas acelera mais rápido?",
            "dica": "Lembre-se da 2ª Lei de Newton: $F = m \\cdot a \\implies a = F / m$.",
            "resposta": "A nave mais leve! Como sua massa ($m$) é menor, para a mesma força ($F$), sua aceleração ($a$) será exatamente o dobro da nave pesada."
        },
        {
            "enigma": "⏳ Se você passar 2 horas orbitando a borda do horizonte de eventos de um buraco negro supermassivo e depois voltar para a Terra, seus amigos estarão mais jovens, com a mesma idade ou muito mais velhos que você?",
            "dica": "A gravidade extrema curva o espaço-tempo e desacelera o relógio do viajante.",
            "resposta": "Seus amigos estarão muito mais velhos (ou até já terão se passado décadas ou séculos na Terra)! Isso é a Dilatação Gravitacional do Tempo de Einstein."
        }
    ],
    "Matemática": [
        {
            "enigma": "📐 A luz viaja a $300.000\\text{ km/s}$. A distância média da Terra à Lua é de aproximadamente $384.000\\text{ km}$. Quanto tempo leva para um sinal de laser disparado da Terra refletir na Lua e voltar para cá?",
            "dica": "Calcule a ida e volta: Distância total = $2 \\times 384.000\\text{ km}$. Tempo = $\\text{Distância} / \\text{Velocidade}$.",
            "resposta": "Aproximadamente **$2,56\\text{ segundos}$** ($1,28\\text{s}$ para ir + $1,28\\text{s}$ para voltar)!"
        },
        {
            "enigma": "🔢 A sonda Voyager 1 está a 24 bilhões de quilômetros da Terra. Como expressamos esse número em Notação Científica padrão?",
            "dica": "24 bilhões = 24.000.000.000 = $2,4 \\times 10^?$.",
            "resposta": "**$2,4 \\times 10^{10}\\text{ km}$** (ou seja, 2,4 multiplicado por 10 elevado à 10ª potência)!"
        }
    ],
    "Química": [
        {
            "enigma": "🧪 O Sol funde 600 milhões de toneladas do elemento mais leve do Universo a cada segundo para produzir o segundo elemento da tabela periódica. Quais são esses dois gases?",
            "dica": "Um tem 1 próton no núcleo e o outro tem 2 prótons.",
            "resposta": "Fusão de **Hidrogênio ($H$)** transformando-se em **Hélio ($He$)** liberando calor e fótons de luz solar!"
        },
        {
            "enigma": "🥔 Para obter água pura em Marte sem levar galões da Terra, qual substância química contendo hidrogênio ($N_2H_4$) Mark Watney decompôs em seu laboratório?",
            "dica": "É um combustível líquido usado nos propulsores de pouso da missão Ares.",
            "resposta": "**Hidrazina ($N_2H_4$)**! Ao quebrar a molécula e queimar o hidrogênio com oxigênio, obtém-se água ($H_2O$)."
        }
    ],
    "Computação": [
        {
            "enigma": "💻 Um sensor térmico do Rover Perseverance enviou o número binário `00001010` para indicar a temperatura. Qual é o valor decimal desse número?",
            "dica": "Os pesos dos bits são 128, 64, 32, 16, 8, 4, 2, 1. Veja quais bits estão ligados em 1.",
            "resposta": "**$10$** (os bits ligados estão nas posições de peso 8 e peso 2: $8 + 2 = 10$)!"
        },
        {
            "enigma": "🤖 Se o Rover precisa desenhar uma estrela de 5 pontas no solo de Marte, qual estrutura de programação evita que o engenheiro tenha que escrever 'Avançar e Virar' 5 vezes na mão?",
            "dica": "É um dos 3 pilares da lógica de programação.",
            "resposta": "Um **Laço de Repetição (Loop / `FOR` ou `WHILE`)** com 5 iterações!"
        }
    ],
    "Geral": [
        {
            "enigma": "🪐 Qual é o único planeta do nosso Sistema Solar que é menos denso que a água líquida (ou seja, flutuaria em uma banheira gigante)?",
            "dica": "É o senhor dos anéis gasosos.",
            "resposta": "**Saturno**! Sua densidade média é de apenas $0,687\\text{ g/cm}^3$ (a água é $1,0\\text{ g/cm}^3$)."
        }
    ]
}

def generate_enigma(pillar: str = "Geral") -> dict:
    options = ENIGMAS_DB.get(pillar, ENIGMAS_DB["Geral"])
    chosen = random.choice(options)
    
    text = f"""
**🧩 Enigma:** {chosen['enigma']}

---
💡 **Dica:** *{chosen['dica']}*

---
🎯 **Resposta & Revelação Científica:**
{chosen['resposta']}
"""
    return {"text": text}
