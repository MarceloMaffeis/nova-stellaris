"""
Nova Stellaris - Sistema de Conquistas e Medalhas STEAM
Define todas as insígnias desbloqueáveis para o aluno.
"""

BADGES = {
    "first_login": {
        "id": "first_login",
        "title": "Passaporte Cósmico",
        "category": "Geral",
        "icon": "🚀",
        "description": "Iniciou sua jornada como explorador espacial no Nova Stellaris!",
        "xp_reward": 50,
        "color": "#00d4ff"
    },
    "gravity_explorer": {
        "id": "gravity_explorer",
        "title": "Mestre da Gravidade",
        "category": "Física",
        "icon": "⚖️",
        "description": "Calculou seu peso em pelo menos 5 mundos diferentes no Observatório!",
        "xp_reward": 100,
        "color": "#9d4edd"
    },
    "martian_botanist": {
        "id": "martian_botanist",
        "title": "Botânico de Marte",
        "category": "Química & Missões",
        "icon": "🥔",
        "description": "Produziu água sintética e calculou a dieta de sobrevivência em Marte!",
        "xp_reward": 150,
        "color": "#ff6b6b"
    },
    "pathfinder_hacker": {
        "id": "pathfinder_hacker",
        "title": "Hacker da Pathfinder",
        "category": "Computação",
        "icon": "💾",
        "description": "Decodificou mensagens em Hexadecimal enviadas pela sonda marciana!",
        "xp_reward": 150,
        "color": "#00f5d4"
    },
    "rocky_friend": {
        "id": "rocky_friend",
        "title": "Amigo de Rocky",
        "category": "Física & Som",
        "icon": "🤝",
        "description": "Dominou a gravidade artificial e a comunicação harmônica de Devoradores de Estrelas!",
        "xp_reward": 150,
        "color": "#ffd166"
    },
    "time_traveler": {
        "id": "time_traveler",
        "title": "Viajante do Tempo de Miller",
        "category": "Física Relativística",
        "icon": "⏳",
        "description": "Calculou a dilatação temporal de Interestelar próxima a um buraco negro!",
        "xp_reward": 150,
        "color": "#7209b7"
    },
    "stellar_chemist": {
        "id": "stellar_chemist",
        "title": "Alquimista das Estrelas",
        "category": "Química",
        "icon": "🧪",
        "description": "Descobriu como os elementos do corpo humano foram forjados no coração de supernovas!",
        "xp_reward": 120,
        "color": "#48cae4"
    },
    "rover_commander": {
        "id": "rover_commander",
        "title": "Comandante de Algoritmos",
        "category": "Computação",
        "icon": "🤖",
        "description": "Programou com sucesso a rota autônoma do Rover pelo labirinto de crateras!",
        "xp_reward": 150,
        "color": "#06d6a0"
    },
    "scientific_notation_wizard": {
        "id": "scientific_notation_wizard",
        "title": "Mago das Potências de 10",
        "category": "Matemática",
        "icon": "🧮",
        "description": "Dominou a notação científica e as escalas de anos-luz do cosmos!",
        "xp_reward": 120,
        "color": "#f72585"
    },
    "quiz_cadet": {
        "id": "quiz_cadet",
        "title": "Cadete da Sabedoria",
        "category": "Quiz",
        "icon": "⭐",
        "description": "Acertou 5 perguntas do AstroQuiz no modo Cadete!",
        "xp_reward": 100,
        "color": "#ffb703"
    },
    "quiz_master": {
        "id": "quiz_master",
        "title": "Mestre Astrofísico",
        "category": "Quiz",
        "icon": "👑",
        "description": "Alcançou pontuação perfeita nas perguntas avançadas de Física e Astronomia!",
        "xp_reward": 250,
        "color": "#ffd700"
    },
    "curious_scholar": {
        "id": "curious_scholar",
        "title": "Explorador da Biblioteca",
        "category": "Hub",
        "icon": "📚",
        "description": "Visitou os simuladores 3D e canais educativos no Hub de Conhecimento!",
        "xp_reward": 80,
        "color": "#3a86ff"
    },
    "astro_farmer": {
        "id": "astro_farmer",
        "title": "Agricultor do Domo Marciano",
        "category": "Astro-Valley",
        "icon": "🌾",
        "description": "Cultivou e colheu 10 safras de batatas e vegetais espaciais no Astro-Valley!",
        "xp_reward": 150,
        "color": "#4ade80"
    },
    "energy_pioneer": {
        "id": "energy_pioneer",
        "title": "Pioneiro da Energia Solar",
        "category": "Astro-Valley",
        "icon": "⚡",
        "description": "Manteve a rede de painéis solares e baterias marcianas com 100% de eficiência!",
        "xp_reward": 150,
        "color": "#fbbf24"
    },
    "sol_survivor": {
        "id": "sol_survivor",
        "title": "Sobrevivente dos Sols",
        "category": "Astro-Valley",
        "icon": "🪐",
        "description": "Sobreviveu a mais de 10 Sols no simulador gerenciando oxigênio, água e biomassa!",
        "xp_reward": 200,
        "color": "#f97316"
    },
    "hail_mary_hero": {
        "id": "hail_mary_hero",
        "title": "Herói de Tau Ceti & Rocky",
        "category": "Arcade",
        "icon": "✨",
        "description": "Coletou 10 espécimes de Taumeba e salvou o Sol no jogo Operação Hail Mary!",
        "xp_reward": 200,
        "color": "#ffd166"
    },
    "gargantua_slingshot": {
        "id": "gargantua_slingshot",
        "title": "Piloto de Gargantua",
        "category": "Arcade",
        "icon": "🕳️",
        "description": "Completou a manobra de estilingue gravitacional e cruzou o Wormhole em Interestelar!",
        "xp_reward": 200,
        "color": "#c084fc"
    },
    "steam_math_master": {
        "id": "steam_math_master",
        "title": "Mestre da Matemática Espacial",
        "category": "Academia STEAM",
        "icon": "📐",
        "description": "Dominou escalas cósmicas, notação científica e leis orbitais de Kepler na Academia!",
        "xp_reward": 180,
        "color": "#38bdf8"
    },
    "steam_phys_master": {
        "id": "steam_phys_master",
        "title": "Físico Cósmico de Vanguarda",
        "category": "Academia STEAM",
        "icon": "⚛️",
        "description": "Dominou gravitação universal, propulsão de foguetes e dilatação temporal relativística!",
        "xp_reward": 180,
        "color": "#a855f7"
    },
    "steam_chem_master": {
        "id": "steam_chem_master",
        "title": "Alquimista do Cosmos",
        "category": "Academia STEAM",
        "icon": "🧪",
        "description": "Dominou a forja de elementos estelares, síntese de compostos em Marte e espectroscopia!",
        "xp_reward": 180,
        "color": "#34d399"
    },
    "steam_tech_master": {
        "id": "steam_tech_master",
        "title": "Engenheiro de Telecom & IA",
        "category": "Academia STEAM",
        "icon": "💻",
        "description": "Dominou algoritmos de sondas, sinais binários da Deep Space Network e IA astronômica!",
        "xp_reward": 180,
        "color": "#fbbf24"
    },
    "steam_polymath": {
        "id": "steam_polymath",
        "title": "Polímata das Galáxias",
        "category": "Academia STEAM",
        "icon": "👑",
        "description": "Conquistou excelência em todos os níveis das 4 disciplinas da Academia STEAM!",
        "xp_reward": 300,
        "color": "#f43f5e"
    }
}

RANKS = [
    {"level": 1, "title": "Observador de Estrelas", "min_xp": 0, "icon": "🔭", "badge_color": "#94a3b8"},
    {"level": 2, "title": "Cadete Espacial", "min_xp": 200, "icon": "🛰️", "badge_color": "#38bdf8"},
    {"level": 3, "title": "Cientista Marciano", "min_xp": 500, "icon": "🔴", "badge_color": "#fb923c"},
    {"level": 4, "title": "Navegador Interestelar", "min_xp": 1000, "icon": "🚀", "badge_color": "#a855f7"},
    {"level": 5, "title": "Comandante da Frota Científica", "min_xp": 1800, "icon": "🌌", "badge_color": "#ec4899"},
    {"level": 6, "title": "Mestre Astrofísico Lendário", "min_xp": 3000, "icon": "👑", "badge_color": "#eab308"},
]

def get_rank_for_xp(xp: int) -> dict:
    current_rank = RANKS[0]
    next_rank = RANKS[1] if len(RANKS) > 1 else None
    
    for i, r in enumerate(RANKS):
        if xp >= r["min_xp"]:
            current_rank = r
            next_rank = RANKS[i+1] if i+1 < len(RANKS) else None
        else:
            break
            
    progress_pct = 100
    if next_rank:
        xp_in_level = xp - current_rank["min_xp"]
        xp_needed = next_rank["min_xp"] - current_rank["min_xp"]
        progress_pct = min(100, max(0, int((xp_in_level / xp_needed) * 100)))
        
    return {
        "current": current_rank,
        "next": next_rank,
        "progress_pct": progress_pct
    }
