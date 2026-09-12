"""
Nova Stellaris - Hub de Conhecimento Cósmico
Links curados, simuladores 3D online, canais educativos do YouTube e guia de filmes/livros.
"""

import streamlit as st
from database import add_xp, unlock_badge

WEB_SIMULATORS = [
    {
        "title": "NASA Eyes on the Solar System",
        "icon": "🛰️",
        "description": "Navegue pelo Sistema Solar em 3D em tempo real, acompanhando a posição exata de sondas espaciais e planetas!",
        "url": "https://eyes.nasa.gov/apps/solar-system/",
        "tag": "Simulador 3D Oficial"
    },
    {
        "title": "Stellarium Web (Planetário Virtual)",
        "icon": "🔭",
        "description": "Veja o céu noturno ao vivo da sua cidade! Identifique constelações, planetas visíveis e satélites artificiais.",
        "url": "https://stellarium-web.org/",
        "tag": "Astronomia Prática"
    },
    {
        "title": "Solar System Scope 3D",
        "icon": "🪐",
        "description": "Modelo tridimensional interativo do sol, órbitas e luas com texturas de alta resolução da NASA.",
        "url": "https://www.solarsystemscope.com/",
        "tag": "Interativo"
    },
    {
        "title": "PhET Simulações: Gravidade e Órbitas",
        "icon": "⚖️",
        "description": "Laboratório virtual interativo da Universidade do Colorado para testar órbitas, gravidade e colisões planetárias.",
        "url": "https://phet.colorado.edu/pt_BR/simulations/gravity-and-orbits",
        "tag": "Laboratório Virtual"
    }
]

YOUTUBE_CHANNELS = [
    {
        "name": "Space Today (Sérgio Sacani)",
        "icon": "🚀",
        "description": "O maior canal de astronomia e astronáutica do Brasil. Notícias diárias, imagens do James Webb e lançamentos de foguetes!",
        "url": "https://www.youtube.com/@SpaceToday",
        "focus": "Astronomia, Missões Espaciais e Geologia Planetária"
    },
    {
        "name": "Ciência Todo Dia (Pedro Loos)",
        "icon": "🧠",
        "description": "Vídeos fascinantes que explicam relatividade, buracos negros, mecânica quântica e matemática de forma clara e instigante.",
        "url": "https://www.youtube.com/@CienciaTodoDia",
        "focus": "Física Teórica, Astrofísica e Matemática"
    },
    {
        "name": "Kurzgesagt – Em Poucas Palavras (Brasil)",
        "icon": "🦆",
        "description": "Animações deslumbrantes sobre a escala do universo, a morte de estrelas, buracos negros e os mistérios do tempo.",
        "url": "https://www.youtube.com/@kurzgesagt_br",
        "focus": "Cosmologia, Biologia Espacial e Filosofia Científica"
    },
    {
        "name": "Manual do Mundo (Iberê Thenório)",
        "icon": "🔬",
        "description": "Experiências científicas práticas, robótica, química divertida e desafios de engenharia.",
        "url": "https://www.youtube.com/@manualdomundo",
        "focus": "Química Prática, Engenharia e Experimentos"
    },
    {
        "name": "NASA Video & Live Streams",
        "icon": "🇺🇸",
        "description": "Transmissões oficiais da Estação Espacial Internacional (ISS), caminhadas espaciais e descobertas em alta definição.",
        "url": "https://www.youtube.com/@NASA",
        "focus": "Transmissões ao Vivo e Documentários Oficiais"
    }
]

MEDIA_GUIDE = [
    {
        "title": "Devoradores de Estrelas (Project Hail Mary)",
        "type": "Livro / Futuro Filme",
        "author": "Andy Weir",
        "science_highlights": "Química de massas, gravidade por aceleração centrífuga, relatividade de Einstein e astrobiologia.",
        "quote": "'Você dorme. Eu vigio. Fist my bump! 👊'"
    },
    {
        "title": "Perdido em Marte (The Martian)",
        "type": "Livro & Filme",
        "author": "Andy Weir / Ridley Scott",
        "science_highlights": "Botânica no solo marciano, cálculo de calorias, estequiometria química de água ($2H_2 + O_2$) e código hexadecimal.",
        "quote": "'Eu vou ter que usar a ciência para sair dessa!'"
    },
    {
        "title": "Interestelar (Interstellar)",
        "type": "Filme",
        "author": "Christopher Nolan & Kip Thorne (Nobel de Física)",
        "science_highlights": "Relatividade Geral, dilatação gravitacional do tempo, lentes gravitacionais ao redor de buracos negros e física de marés.",
        "quote": "'O amor é a única coisa que somos capazes de perceber que transcende as dimensões de tempo e espaço.'"
    },
    {
        "title": "Cosmos: Uma Viagem Pessoal / Possíveis Mundos",
        "type": "Série Documental",
        "author": "Carl Sagan / Neil deGrasse Tyson",
        "science_highlights": "A história da evolução do pensamento científico, a escala do tempo cósmico e o papel da humanidade no universo.",
        "quote": "'Somos todos poeira de estrelas.'"
    }
]

def render_knowledge_hub(user: dict):
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(16,30,60,0.95), rgba(16,20,47,0.95)); border: 1px solid #3a86ff;'>
            <h1 style='color: #38bdf8; margin-bottom: 5px;'>📚 Hub de Conhecimento Espacial</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Os melhores simuladores 3D online, canais educativos do YouTube e guias de ficção científica para continuar aprendendo!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🪐 Simuladores 3D Web", "📺 Canais do YouTube", "🎬 Livros & Filmes STEAM"])
    
    # ----------------------------------------------------
    # TAB 1: SIMULADORES 3D
    # ----------------------------------------------------
    with tab1:
        st.subheader("🪐 Simuladores Virtuais Gratuitos na Web")
        st.markdown("Clique nos links para abrir simuladores interativos em 3D diretamente no seu navegador:")
        
        for sim in WEB_SIMULATORS:
            st.markdown(f"""
                <div class='cosmic-card' style='border-left: 4px solid #00d4ff;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <h3 style='margin: 0; color: #00d4ff;'>{sim['icon']} {sim['title']}</h3>
                        <span class='steam-tag' style='background: rgba(0,212,255,0.2); color: #00d4ff; border: 1px solid #00d4ff;'>{sim['tag']}</span>
                    </div>
                    <p style='color: #cbd5e1; margin-top: 10px;'>{sim['description']}</p>
                    <a href='{sim['url']}' target='_blank' style='display: inline-block; background: #00d4ff; color: #0b0d19; font-weight: 700; padding: 8px 18px; border-radius: 8px; text-decoration: none; margin-top: 5px;'>Abrir Simulador ➔</a>
                </div>
            """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 2: CANAIS DO YOUTUBE
    # ----------------------------------------------------
    with tab2:
        st.subheader("📺 Melhores Canais Educativos de Ciência")
        
        for ch in YOUTUBE_CHANNELS:
            st.markdown(f"""
                <div class='cosmic-card' style='border-left: 4px solid #f72585;'>
                    <h3 style='margin: 0; color: #ffd166;'>{ch['icon']} {ch['name']}</h3>
                    <p style='color: #cbd5e1; margin-top: 8px;'>{ch['description']}</p>
                    <p style='font-size: 0.85rem; color: #94a3b8;'><strong>Foco Principal:</strong> {ch['focus']}</p>
                    <a href='{ch['url']}' target='_blank' style='display: inline-block; background: #f72585; color: #ffffff; font-weight: 700; padding: 6px 16px; border-radius: 8px; text-decoration: none; margin-top: 5px;'>Visitar Canal no YouTube ➔</a>
                </div>
            """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 3: LIVROS & FILMES
    # ----------------------------------------------------
    with tab3:
        st.subheader("🎬 Obras-Primas da Ficção Científica Rigorosa")
        
        for m in MEDIA_GUIDE:
            st.markdown(f"""
                <div class='cosmic-card' style='border-left: 4px solid #ffd166;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <h3 style='margin: 0; color: #ffd166;'>{m['title']}</h3>
                        <span style='color: #94a3b8; font-size: 0.9rem;'>{m['type']} • {m['author']}</span>
                    </div>
                    <p style='margin-top: 10px;'>🔬 <strong>Ciência & STEAM em Destaque:</strong> {m['science_highlights']}</p>
                    <blockquote style='border-left: 3px solid #06d6a0; padding-left: 10px; color: #06d6a0; font-style: italic; margin: 10px 0;'>
                        {m['quote']}
                    </blockquote>
                </div>
            """, unsafe_allow_html=True)
            
    # Conquista do Hub
    if unlock_badge(user["id"], "curious_scholar"):
        add_xp(user["id"], 80)
        st.balloons()
        st.success("🎉 **Conquista Desbloqueada:** 📚 Explorador da Biblioteca! (+80 XP)")
