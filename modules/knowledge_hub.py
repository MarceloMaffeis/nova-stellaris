"""
Nova Stellaris - Grande Hub & Biblioteca Cósmica
Enciclopédia de Pesquisa, Galeria de Cientistas Pioneiros, Guia de Observação Noturna,
Catálogo de Missões e Telescópios da NASA/ESA, Simuladores e Recursos Educacionais.
"""

import os
import base64
import streamlit as st
from database import add_xp, unlock_badge

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")

def get_img(filename: str) -> str:
    local_p = os.path.join(IMG_DIR, filename)
    if os.path.exists(local_p):
        return local_p
    return filename

def get_image_src(image_path_or_url: str) -> str:
    """Converte imagem local para data URI em Base64 para garantir exibição impecável no Streamlit."""
    if os.path.exists(image_path_or_url):
        ext = os.path.splitext(image_path_or_url)[1].lower().replace(".", "")
        if ext == "jpg":
            ext = "jpeg"
        try:
            with open(image_path_or_url, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/{ext};base64,{encoded}"
        except Exception:
            pass
    return image_path_or_url

# ----------------------------------------------------------------------
# 1. ENCICLOPÉDIA DE TERMOS E CONCEITOS (BASE DE PESQUISA)
# ----------------------------------------------------------------------
ENCYCLOPEDIA_TERMS = {
    "Ano-Luz (Light-Year)": {
        "categoria": "Distâncias Cósmicas",
        "resumo": "A distância que um raio de luz percorre no vácuo durante 1 ano terrestre inteiro.",
        "detalhes": "Como a luz viaja a incríveis 300.000 km/s, em um ano ela percorre aproximadamente 9,46 trilhões de quilômetros (9,46 x 10^12 km)! O ano-luz é uma unidade de DISTÂNCIA, não de tempo.",
        "exemplo": "A estrela mais próxima da Terra (fora o Sol), chamada Próxima Centauri, fica a 4,24 anos-luz de distância.",
        "icone": "✨"
    },
    "Buraco Negro (Black Hole)": {
        "categoria": "Astrofísica Extrema",
        "resumo": "Uma região do espaço onde a gravidade é tão descomunalmente forte que absolutamente nada — nem mesmo a luz — consegue escapar de dentro dela.",
        "detalhes": "Formam-se quando estrelas hipergigantes morrem e colapsam sobre si mesmas. A fronteira de não retorno é chamada de Horizonte de Eventos, cujo tamanho é dado pelo Raio de Schwarzschild (Rs = 2GM/c²).",
        "exemplo": "No centro da nossa galáxia existe um buraco negro supermassivo chamado Sagittarius A*, com massa de 4 milhões de vezes a massa do Sol!",
        "icone": "🕳️"
    },
    "Supernova": {
        "categoria": "Evolução Estelar",
        "resumo": "A explosão monumental e brilhante que marca a morte cataclísmica de uma estrela massiva.",
        "detalhes": "Durante alguns dias ou semanas, uma única supernova pode brilhar mais do que uma galáxia inteira com 100 bilhões de estrelas! É durante a supernova que os elementos químicos mais pesados (como ferro, ouro e platina) são forjados e espalhados pelo espaço.",
        "exemplo": "A famosa Nebulosa do Caranguejo é o remanescente de uma supernova que explodiu e foi registrada por astrônomos chineses no ano 1054 d.C.",
        "icone": "💥"
    },
    "Exoplaneta": {
        "categoria": "Planetas & Sistemas Solares",
        "resumo": "Qualquer planeta que orbita uma estrela que NÃO seja o nosso Sol.",
        "detalhes": "Até hoje, telescópios como Kepler, TESS e James Webb já confirmaram mais de 5.500 exoplanetas em nossa galáxia! Os principais métodos para descobri-los são o Método do Trânsito (queda de brilho estelar) e a Velocidade Radial.",
        "exemplo": "O sistema TRAPPIST-1 possui 7 planetas rochosos de tamanho parecido com o da Terra orbitando uma estrela anã vermelha.",
        "icone": "🪐"
    },
    "Fusão Nuclear Estelar": {
        "categoria": "Física Quântica & Estrelas",
        "resumo": "O processo que faz as estrelas brilharem: núcleos de átomos leves se fundem para criar átomos mais pesados, liberando quantidades colossais de energia.",
        "detalhes": "No núcleo do Sol, sob temperaturas de 15 milhões de graus Celsius, 4 átomos de Hidrogênio se fundem para formar 1 átomo de Hélio a cada ciclo. A diferença de massa se transforma em luz e calor pela famosa equação de Einstein E = mc².",
        "exemplo": "Cientistas na Terra estão tentando recriar a fusão nuclear em reatores chamados Tokamaks (como o projeto ITER) para gerar energia limpa e infinita.",
        "icone": "☀️"
    },
    "Matéria Escura": {
        "categoria": "Cosmologia & Física",
        "resumo": "Um tipo misterioso e invisível de matéria que não emite, não absorve e não reflete luz, mas cuja gravidade mantém as galáxias unidas.",
        "detalhes": "A astrônoma Vera Rubin descobriu que as estrelas nas bordas das galáxias giram muito mais rápido do que a matéria visível permitiria. Estima-se que a matéria escura componha cerca de 85% de toda a massa do Universo!",
        "exemplo": "Nós sabemos que ela existe porque sua imensa gravidade desvia o caminho dos raios de luz de galáxias de fundo (efeito de lente gravitacional).",
        "icone": "🌌"
    },
    "Paralaxe Trigonométrica": {
        "categoria": "Matemática & Medição",
        "resumo": "O método geométrico usado para calcular a distância exata de estrelas próximas usando o movimento orbital da Terra.",
        "detalhes": "Observa-se uma estrela em janeiro e depois em julho (base de 2 UA). O pequeno desvio angular aparente 'p' (em segundos de arco) dá a distância 'd' diretamente em parsecs: d = 1 / p.",
        "exemplo": "O satélite espacial Gaia da ESA mediu a paralaxe de mais de 1 bilhão de estrelas com precisão microscópica!",
        "icone": "📐"
    },
    "Velocidade de Escape": {
        "categoria": "Física & Foguetes",
        "resumo": "A velocidade mínima necessária para que um corpo (como um foguete ou projétil) se liberte completamente da atração gravitacional de um astro sem precisar de mais propulsão.",
        "detalhes": "A fórmula é v = sqrt(2 * G * M / R). Na superfície da Terra, a velocidade de escape é de aproximadamente 11,2 km/s (mais de 40.000 km/h!). Na Lua é de apenas 2,4 km/s.",
        "exemplo": "Para enviar sondas como a New Horizons para Plutão, os foguetes precisam atingir a velocidade de escape terrestre.",
        "icone": "🚀"
    },
    "Nebulosa": {
        "categoria": "Estruturas Cósmicas",
        "resumo": "Uma imensa nuvem interestelar de poeira cósmica, gás hidrogênio e plasma no espaço.",
        "detalhes": "As nebulosas são chamadas de 'berçários estelares' porque é dentro delas que o gás se condensa pela gravidade para formar novas estrelas e sistemas solares.",
        "exemplo": "A Nebulosa de Órion (M42) pode ser vista a olho nu em noites escuras logo abaixo do cinturão de Órion (Três Marias).",
        "icone": "🌫️"
    },
    "Ondas Gravitacionais": {
        "categoria": "Astrofísica Relativística",
        "resumo": "Ondulações e vibrações no próprio tecido do espaço-tempo que se propagam na velocidade da luz.",
        "detalhes": "Previstas por Albert Einstein em 1916 e detectadas diretamente pela primeira vez em 2015 pelo observatório LIGO quando dois buracos negros colidiram a mais de 1 bilhão de anos-luz de nós.",
        "exemplo": "A detecção abriu a era da 'Astronomia de Multimensageiros', permitindo que a humanidade 'ouça' os choques mais violentos do Cosmos.",
        "icone": "🌊"
    },
    "Cinturão de Kuiper & Nuvem de Oort": {
        "categoria": "Fronteiras do Sistema Solar",
        "resumo": "Regiões geladas e distantes repletas de milhares de corpos rochosos congelados, planetas anões e cometas.",
        "detalhes": "O Cinturão de Kuiper fica logo após a órbita de Netuno (onde mora Plutão). A Nuvem de Oort é uma concha esférica colossal que envolve todo o Sistema Solar até quase 1 ano-luz do Sol.",
        "exemplo": "Os cometas de longo período que vemos cruzar o céu com suas caudas brilhantes vêm da Nuvem de Oort.",
        "icone": "☄️"
    },
    "Radiação Cósmica de Fundo (CMB)": {
        "categoria": "Cosmologia",
        "resumo": "O 'eco' ou brilho residual do Big Bang que permeia todo o Universo observável.",
        "detalhes": "Emitida quando o Universo tinha cerca de 380.000 anos e os primeiros átomos neutros de hidrogênio se formaram, permitindo que a luz viajasse livremente. Sua temperatura hoje é de apenas 2,7 Kelvin (-270,45 °C).",
        "exemplo": "Uma pequena porcentagem do chiado preto-e-branco das televisões analógicas antigas era provocada por essa radiação primordial do Big Bang!",
        "icone": "📻"
    }
}

# ----------------------------------------------------------------------
# 2. GRANDES CIENTISTAS E PIONEIROS (COM FOTOS LIVRES WIKIMEDIA)
# ----------------------------------------------------------------------
PIONEER_SCIENTISTS = [
    {
        "nome": "Carl Sagan (1934 – 1996)",
        "titulo": "Astrobiólogo, Divulgador & Poeta do Cosmos",
        "pais": "🇺🇸 Estados Unidos",
        "foto": get_img("carl_sagan.jpg"),
        "conquistas": "Apresentou a icônica série 'Cosmos', idealizou o Disco de Ouro das sondas Voyager e ensinou a humanidade a olhar para as estrelas com rigor científico e deslumbramento.",
        "frase": "'Diante da vastidão do tempo e da imensidão do universo, é um privilégio compartilhar um planeta e uma era com você.'"
    },
    {
        "nome": "Katherine Johnson (1918 – 2020)",
        "titulo": "Matemática & Física Espacial da NASA",
        "pais": "🇺🇸 Estados Unidos",
        "foto": get_img("katherine_johnson.jpg"),
        "conquistas": "Calculou manualmente com precisão impecável as trajetórias orbitais do voo de John Glenn e da missão Apollo 11 que levou o homem à Lua. Sua história inspirou o livro e filme 'Estrelas Além do Tempo'.",
        "frase": "'Eu gostava de matemática. Contava tudo: os passos que dava, os pratos que lavava... tudo o que podia ser contado.'"
    },
    {
        "nome": "Johannes Kepler (1571 – 1630)",
        "titulo": "Astrônomo e Matemático Alemão",
        "pais": "🇩🇪 Alemanha",
        "foto": get_img("johannes_kepler.jpg"),
        "conquistas": "Descobriu as 3 Leis do Movimento Planetário, provando que as órbitas dos planetas não são círculos perfeitos, mas elipses, e estabeleceu a fórmula harmônica T² = a³.",
        "frase": "'A geometria existia antes da Criação. Ela é eterna como o próprio pensamento divino.'"
    },
    {
        "nome": "Marie Curie (1867 – 1934)",
        "titulo": "Física e Química Pioneira (2 Prêmios Nobel)",
        "pais": "🇵🇱 Polônia / 🇫🇷 França",
        "foto": get_img("marie_curie.jpg"),
        "conquistas": "Descobriu os elementos químicos Polônio e Rádio, fundou o estudo da radioatividade (essencial para entender o calor interno de planetas e a energia de estrelas) e foi a primeira pessoa a ganhar dois prêmios Nobel em ciências distintas!",
        "frase": "'Nada na vida deve ser temido, apenas compreendido. Agora é a hora de compreender mais, para temer menos.'"
    },
    {
        "nome": "Albert Einstein (1879 – 1955)",
        "titulo": "Físico Teórico & Criador da Relatividade",
        "pais": "🇩🇪 Alemanha / 🇨🇭 Suíça / 🇺🇸 EUA",
        "foto": get_img("albert_einstein.jpg"),
        "conquistas": "Formulou a Teoria da Relatividade Especial (E = mc²) e a Teoria da Relatividade Geral, mostrando que a gravidade é a curvatura do espaço-tempo provocada pela massa. Previu buracos negros e ondas gravitacionais.",
        "frase": "'A imaginação é mais importante que o conhecimento, pois o conhecimento é limitado, enquanto a imaginação abraça todo o Universo.'"
    },
    {
        "nome": "Stephen Hawking (1942 – 2018)",
        "titulo": "Físico Teórico e Cosmólogo",
        "pais": "🇬🇧 Reino Unido",
        "foto": get_img("stephen_hawking.jpg"),
        "conquistas": "Descobriu a Radiação Hawking (mostrando que buracos negros emitem radiação e evaporam lentamente), escreveu o best-seller 'Uma Breve História do Tempo' e desvendou a origem do Universo e singularidades quânticas.",
        "frase": "'Lembre-se de olhar para as estrelas e não para baixo, para os seus pés. Seja curioso.'"
    },
    {
        "nome": "Vera Rubin (1928 – 2016)",
        "titulo": "Astrônoma Pioneira da Matéria Escura",
        "pais": "🇺🇸 Estados Unidos",
        "foto": get_img("vera_rubin.jpg"),
        "conquistas": "Observou a curva de rotação de dezenas de galáxias espirais e forneceu a primeira evidência observacional conclusiva da existência da Matéria Escura no Universo. O maior observatório astronômico do Chile (Vera C. Rubin Observatory) foi batizado em sua homenagem!",
        "frase": "'A ciência é como caminhar em uma floresta escura com uma pequena lanterna. A cada passo, o mistério aumenta.'"
    },
    {
        "nome": "Cecilia Payne-Gaposchkin (1900 – 1979)",
        "titulo": "Astrofísica britânica-americana",
        "pais": "🇬🇧 Reino Unido / 🇺🇸 EUA",
        "foto": get_img("cecilia_payne.jpg"),
        "conquistas": "Descobriu em sua tese de doutorado em Harvard (1925) que o Sol e as estrelas são compostos quase inteiramente de Hidrogênio e Hélio, corrigindo todo o entendimento da ciência da época!",
        "frase": "'A recompensa do jovem cientista é a emoção emocional de ser a primeira pessoa na história a ver algo novo.'"
    }
]

# ----------------------------------------------------------------------
# 3. GRANDES TELESCÓPIOS E MISSÕES ESPACIAIS
# ----------------------------------------------------------------------
FAMOUS_MISSIONS = [
    {
        "nome": "Telescópio Espacial James Webb (JWST)",
        "tipo": "Observatório Espacial Infravermelho",
        "foto": get_img("jwst.png"),
        "orbita": "Ponto de Lagrange L2 (1,5 milhão de km da Terra)",
        "missao": "O maior e mais poderoso telescópio espacial já construído. Com espelho banhado a ouro de 6,5 metros, ele enxerga através da poeira cósmica no infravermelho para registrar as primeiras galáxias formadas após o Big Bang e analisar atmosferas de exoplanetas."
    },
    {
        "nome": "Telescópio Espacial Hubble (HST)",
        "tipo": "Observatório Espacial Óptico e Ultravioleta",
        "foto": get_img("hubble.jpg"),
        "orbita": "Órbita Baixa da Terra (540 km de altitude)",
        "missao": "Lançado em 1990, revolucionou a astronomia ao fornecer imagens ultra nítidas e deslumbrantes livres da turbulência da atmosfera da Terra. Ajudou a determinar a idade precisa do Universo (13,8 bilhões de anos)."
    },
    {
        "nome": "Rover Perseverance & Helicóptero Ingenuity",
        "tipo": "Laboratório Robótico em Marte",
        "foto": get_img("perseverance.jpg"),
        "orbita": "Cratera Jezero, Planeta Marte",
        "missao": "Pousou em Marte em 2021 em busca de sinais de antiga vida microbiana fóssil, coletando amostras de rochas em tubos de titânio e testando a produção autônoma de oxigênio (MOXIE) na atmosfera marciana."
    },
    {
        "nome": "Sondas Voyager 1 & Voyager 2",
        "tipo": "Exploração Interestelar Profunda",
        "foto": get_img("voyager.png"),
        "orbita": "Espaço Interestelar (a mais de 24 bilhões de km da Terra)",
        "missao": "Lançadas em 1977, exploraram Júpiter, Saturno, Urano e Netuno e agora são os objetos feitos pelo ser humano mais distantes no Cosmos, carregando o Disco de Ouro com sons e fotos da Terra."
    },
    {
        "nome": "Estação Espacial Internacional (ISS)",
        "tipo": "Laboratório Científico Orbital Habitado",
        "foto": get_img("iss.jpg"),
        "orbita": "Órbita Baixa (400 km de altitude, 28.000 km/h)",
        "missao": "Um laboratório habitado continuamente há mais de 20 anos onde astronautas realizam experimentos de microgravidade, biologia, física e medicina. Dá uma volta completa na Terra a cada 90 minutos (16 pores do sol por dia!)."
    }
]

# ----------------------------------------------------------------------
# 4. RENDER PRINCIPAL DO MÓDULO
# ----------------------------------------------------------------------
def render_knowledge_hub(user: dict, default_subtab: str = None, *args, **kwargs):
    if not default_subtab:
        default_subtab = st.session_state.get("knowledge_subtab_default")
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(16,28,60,0.95), rgba(12,18,40,0.95)); border: 1px solid #00d4ff;'>
            <h1 style='color: #00d4ff; margin-bottom: 5px;'>📚 Grande Biblioteca Cósmica & Enciclopédia</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Seu centro completo de pesquisa astronômica: consulte termos científicos, conheça os grandes cientistas, explore missões espaciais e aprenda a observar o céu!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    sub_options = [
        "🔍 Enciclopédia & Glossário",
        "👩‍🔬 Grandes Cientistas",
        "🛰️ Missões & Telescópios",
        "🔭 Guia de Observação do Céu",
        "🌐 Simuladores & Canais Oficiais"
    ]
    
    default_idx = 0
    if default_subtab:
        for i, opt in enumerate(sub_options):
            if default_subtab.lower() in opt.lower():
                default_idx = i
                break
    elif "knowledge_subtab_idx" in st.session_state:
        default_idx = st.session_state.knowledge_subtab_idx

    active_tab = st.radio(
        "Navegação da Biblioteca:",
        sub_options,
        index=default_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="knowledge_subtab_selector"
    )
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 1: ENCICLOPÉDIA DE PESQUISA
    # ----------------------------------------------------
    if active_tab == sub_options[0]:
        st.subheader("🔍 Enciclopédia de Termos & Conceitos Astronômicos")
        st.write("Digite uma palavra-chave para pesquisar ou explore as categorias abaixo:")
        
        search_query = st.text_input("🔎 Pesquisar conceito astronômico (ex: Buraco Negro, Paralaxe, Supernova, Exoplaneta, Fusão):", "", key="encyclopedia_search")
        
        categories = ["Todas as Categorias"] + list(set(item["categoria"] for item in ENCYCLOPEDIA_TERMS.values()))
        cat_filter = st.selectbox("Filtrar por Categoria Temática:", categories, key="encyclopedia_cat")
        
        filtered_terms = {}
        for name, data in ENCYCLOPEDIA_TERMS.items():
            matches_search = (
                search_query.lower() in name.lower() or 
                search_query.lower() in data["resumo"].lower() or 
                search_query.lower() in data["detalhes"].lower()
            ) if search_query else True
            
            matches_cat = (cat_filter == "Todas as Categorias" or data["categoria"] == cat_filter)
            
            if matches_search and matches_cat:
                filtered_terms[name] = data
                
        if not filtered_terms:
            st.info(f"Nenhum termo encontrado para '{search_query}'. Tente pesquisar por termos como: *Ano-Luz, Buraco Negro, Exoplaneta, Supernova, Gravidade*.")
        else:
            st.markdown(f"**{len(filtered_terms)} conceitos encontrados:**")
            
            for term_name, t_data in filtered_terms.items():
                with st.expander(f"{t_data['icone']} {term_name} — {t_data['resumo']}", expanded=bool(search_query)):
                    st.markdown(f"""
                        <div style='background: rgba(19, 23, 43, 0.7); border-left: 4px solid #00d4ff; padding: 14px 18px; border-radius: 8px; margin-bottom: 10px;'>
                            <span class='steam-tag' style='background: rgba(0,212,255,0.15); color: #38bdf8;'>📁 {t_data['categoria']}</span>
                            <h4 style='color: #00d4ff; margin: 8px 0 4px 0;'>{term_name}</h4>
                            <p style='color: #f1f5f9; font-size: 0.95rem; line-height: 1.5;'>{t_data['detalhes']}</p>
                            <p style='color: #ffd166; font-size: 0.9rem; margin: 0;'><strong>💡 Exemplo Real no Cosmos:</strong> {t_data['exemplo']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
        st.markdown("---")
        st.caption("✨ Dica: Você também pode perguntar qualquer dúvida aprofundada para o seu mentor de IA na aba **🤖 CosmoAI**!")

    # ----------------------------------------------------
    # TAB 2: GRANDES CIENTISTAS (GALERIA COM FOTOS LOCAIS)
    # ----------------------------------------------------
    elif active_tab == sub_options[1]:
        st.subheader("👩‍🔬 Galeria dos Grandes Pioneiros da Ciência & Astronomia")
        st.write("Conheça as mentes brilhantes que decifraram os mistérios das leis do Universo e abriram o caminho para a exploração espacial:")
        
        c_sci1, c_sci2 = st.columns(2)
        
        for idx, sci in enumerate(PIONEER_SCIENTISTS):
            target_col = c_sci1 if idx % 2 == 0 else c_sci2
            photo_src = get_image_src(sci['foto'])
            
            with target_col:
                with st.container():
                    st.markdown(f"""
                        <div class='cosmic-card' style='margin-bottom: 20px;'>
                            <div style='display: flex; gap: 16px; align-items: flex-start;'>
                                <img src='{photo_src}' alt='{sci['nome']}' style='width: 110px; height: 130px; object-fit: cover; border-radius: 12px; border: 2px solid #00d4ff; box-shadow: 0 4px 15px rgba(0,212,255,0.25); background: #0f172a;'>
                                <div>
                                    <h3 style='color: #00d4ff; margin: 0 0 2px 0; font-size: 1.15rem;'>{sci['nome']}</h3>
                                    <span style='color: #94a3b8; font-size: 0.85rem; font-weight: 600;'>{sci['pais']}</span><br>
                                    <span style='color: #ffd166; font-size: 0.85rem; font-weight: 700;'>{sci['titulo']}</span>
                                </div>
                            </div>
                            <div style='margin-top: 12px; color: #cbd5e1; font-size: 0.9rem; line-height: 1.4;'>
                                <p><strong>🏆 Contribuição:</strong> {sci['conquistas']}</p>
                                <blockquote style='border-left: 3px solid #9d4edd; padding-left: 10px; color: #e2e8f0; font-style: italic; margin: 8px 0;'>{sci['frase']}</blockquote>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 3: MISSÕES & TELESCÓPIOS
    # ----------------------------------------------------
    elif active_tab == sub_options[2]:
        st.subheader("🛰️ Catálogo de Grandes Missões & Telescópios Espaciais")
        st.write("Veja as maravilhas da engenharia que a humanidade lançou no espaço para tocar os planetas e fotografar a aurora do tempo:")
        
        for miss in FAMOUS_MISSIONS:
            photo_src = get_image_src(miss['foto'])
            with st.container():
                st.markdown(f"""
                    <div class='cosmic-card' style='margin-bottom: 22px;'>
                        <div style='display: flex; gap: 20px; align-items: center; flex-wrap: wrap;'>
                            <img src='{photo_src}' alt='{miss['nome']}' style='width: 220px; height: 150px; object-fit: cover; border-radius: 12px; border: 1px solid rgba(0,212,255,0.4); box-shadow: 0 6px 20px rgba(0,0,0,0.5); background: #0f172a;'>
                            <div style='flex: 1; min-width: 260px;'>
                                <span class='steam-tag' style='background: rgba(6,214,160,0.2); color: #06d6a0; border: 1px solid #06d6a0;'>🛰️ {miss['tipo']}</span>
                                <h3 style='color: #00d4ff; margin: 6px 0;'>{miss['nome']}</h3>
                                <p style='color: #ffd166; font-size: 0.85rem; margin: 0 0 8px 0;'><strong>📍 Localização / Órbita:</strong> {miss['orbita']}</p>
                                <p style='color: #e2e8f0; font-size: 0.92rem; line-height: 1.45;'>{miss['missao']}</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 4: GUIA DE OBSERVAÇÃO DO CÉU NOTURNO
    # ----------------------------------------------------
    elif active_tab == sub_options[3]:
        st.subheader("🔭 Guia Prático de Observação do Céu para Alunos")
        st.write("Você não precisa de um telescópio gigante para começar a observar o céu! Veja como identificar astros hoje mesmo da sua janela:")
        
        c_obs1, c_obs2 = st.columns(2)
        
        with c_obs1:
            st.markdown("""
                <div class='cosmic-card'>
                    <h3 style='color: #ffd166; font-size: 1.1rem;'>🌟 1. Estrela ou Planeta? O Truque do Pisca-Pisca!</h3>
                    <p style='color: #cbd5e1; font-size: 0.9rem;'>
                        Quando você olha para um pontinho brilhante no céu noturno, como saber se ele é uma <strong>estrela distante</strong> ou um <strong>planeta do Sistema Solar</strong>?
                    </p>
                    <ul>
                        <li><strong>Estrelas piscam (cintilam):</strong> Como estão a trilhões de km, a luz chega como um feixe finíssimo que é desviado pelas correntes de ar da atmosfera da Terra.</li>
                        <li><strong>Planetas NÃO piscam (luz fixa e estável):</strong> Como estão muito mais perto de nós, sua luz chega como um 'disco', não sofrendo tanta interferência do ar. Se brilhar forte e constante, é um planeta (como Vênus, Júpiter ou Marte)!</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class='cosmic-card'>
                    <h3 style='color: #00d4ff; font-size: 1.1rem;'>🧭 2. Achando o Sul pelo Cruzeiro do Sul</h3>
                    <p style='color: #cbd5e1; font-size: 0.9rem;'>
                        No hemisfério Sul (onde fica o Brasil), a constelação do <strong>Cruzeiro do Sul</strong> é a maior bússola natural:
                    </p>
                    <ol>
                        <li>Localize as 4 estrelas em cruz e a estrela menor no meio (a 'Intrometida').</li>
                        <li>Trace uma linha reta imaginária pelo braço maior da cruz (da estrela de cima até a de baixo).</li>
                        <li>Prolongue essa linha reta <strong>4 vezes e meia (4,5x)</strong> o tamanho da cruz.</li>
                        <li>Desça uma linha vertical até o horizonte: ali fica o <strong>Sul Geográfico verdadeiro</strong>!</li>
                    </ol>
                </div>
            """, unsafe_allow_html=True)
            
        with c_obs2:
            st.markdown("""
                <div class='cosmic-card'>
                    <h3 style='color: #06d6a0; font-size: 1.1rem;'>🌕 3. As 4 Fases da Lua</h3>
                    <p style='color: #cbd5e1; font-size: 0.9rem;'>
                        A Lua não tem luz própria — ela apenas reflete a luz do Sol. Conforme a Lua orbita a Terra a cada 29,5 dias, vemos diferentes porções da face iluminada:
                    </p>
                    <ul>
                        <li><strong>Lua Nova:</strong> A face iluminada está voltada para o Sol (Lua invisível à noite).</li>
                        <li><strong>Quarto Crescente:</strong> Vemos a metade direita iluminada (formato de letra 'D' no hemisfério Sul).</li>
                        <li><strong>Lua Cheia:</strong> A face voltada para a Terra está 100% iluminada pelo Sol.</li>
                        <li><strong>Quarto Minguante:</strong> Vemos a metade esquerda iluminada (formato de letra 'C' no hemisfério Sul).</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class='cosmic-card'>
                    <h3 style='color: #f72585; font-size: 1.1rem;'>🌠 4. Chuvas de Meteoros do Ano</h3>
                    <p style='color: #cbd5e1; font-size: 0.9rem;'>
                        As famosas 'estrelas cadentes' são pequenos grãos de poeira deixados por cometas que queimam na alta atmosfera:
                    </p>
                    <ul>
                        <li><strong>Líridas (Abril):</strong> Pico em 21-22 de abril (~18 meteoros por hora).</li>
                        <li><strong>Perseidas (Agosto):</strong> Pico em 11-13 de agosto (uma das mais intensas, até 100 meteoros/hora).</li>
                        <li><strong>Oriônidas (Outubro):</strong> Poeira do famoso Cometa Halley (pico em 21-22 de outubro).</li>
                        <li><strong>Geminídeas (Dezembro):</strong> A mais brilhante do ano (pico em 13-14 de dezembro, até 120 meteoros/hora).</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 5: SIMULADORES E LINKS OFICIAIS
    # ----------------------------------------------------
    else:
        st.subheader("🌐 Simuladores Virtuais & Canais Oficiais de Ciência")
        st.write("Recursos digitais livres para explorar o cosmos em 3D e acompanhar notícias da astronomia:")
        
        c_link1, c_link2 = st.columns(2)
        
        with c_link1:
            st.markdown("#### 🛰️ Simuladores 3D Interativos Online")
            simulators = [
                ("NASA Eyes on the Solar System", "https://eyes.nasa.gov/apps/solar-system/", "Simulador oficial da NASA em 3D em tempo real com sondas e planetas."),
                ("Stellarium Web Planetário", "https://stellarium-web.org/", "Planetário virtual gratuito para ver o céu ao vivo da sua cidade."),
                ("Solar System Scope 3D", "https://www.solarsystemscope.com/", "Modelo 3D do Sistema Solar com texturas reais de satélites."),
                ("PhET Colorado: Gravidade e Órbitas", "https://phet.colorado.edu/pt_BR/simulations/gravity-and-orbits", "Laboratório interativo da Univ. do Colorado para testar órbitas.")
            ]
            for title, url, desc in simulators:
                st.markdown(f"""
                    <div style='background: rgba(19, 23, 43, 0.7); border: 1px solid rgba(0,212,255,0.3); border-radius: 10px; padding: 12px; margin-bottom: 10px;'>
                        <h4 style='margin: 0;'><a href='{url}' target='_blank' style='color: #00d4ff; text-decoration: none;'>🚀 {title} ↗</a></h4>
                        <p style='color: #cbd5e1; font-size: 0.85rem; margin: 4px 0 0 0;'>{desc}</p>
                    </div>
                """, unsafe_allow_html=True)
                
        with c_link2:
            st.markdown("#### 📺 Canais Educativos Recomendados")
            channels = [
                ("Space Today (Sérgio Sacani)", "https://www.youtube.com/@SpaceToday", "O maior canal de astronomia e astronáutica do Brasil com notícias diárias."),
                ("Ciência Todo Dia (Pedro Loos)", "https://www.youtube.com/@CienciaTodoDia", "Física, astrofísica e matemática explicadas de forma instigante."),
                ("Kurzgesagt – Em Poucas Palavras", "https://www.youtube.com/@kurzgesagt_br", "Animações fantásticas sobre o universo, buracos negros e evolução."),
                ("Manual do Mundo (Iberê Thenório)", "https://www.youtube.com/@manualdomundo", "Experimentos práticos de física, química e robótica."),
                ("NASA Live & Documentaries", "https://www.youtube.com/@NASA", "Transmissões ao vivo da ISS e caminhadas espaciais.")
            ]
            for name, url, desc in channels:
                st.markdown(f"""
                    <div style='background: rgba(19, 23, 43, 0.7); border: 1px solid rgba(157,78,221,0.3); border-radius: 10px; padding: 12px; margin-bottom: 10px;'>
                        <h4 style='margin: 0;'><a href='{url}' target='_blank' style='color: #c77dff; text-decoration: none;'>▶️ {name} ↗</a></h4>
                        <p style='color: #cbd5e1; font-size: 0.85rem; margin: 4px 0 0 0;'>{desc}</p>
                    </div>
                """, unsafe_allow_html=True)
