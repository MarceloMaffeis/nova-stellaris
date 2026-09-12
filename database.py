"""
Nova Stellaris - Banco de Dados SQLite
Gerenciamento de perfis, progresso, XP, insígnias e perguntas STEAM.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "nova_stellaris.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        avatar TEXT DEFAULT '🚀',
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_badges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        badge_id TEXT NOT NULL,
        unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, badge_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pillar TEXT NOT NULL,
        category TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        question TEXT NOT NULL,
        options_json TEXT NOT NULL,
        correct_idx INTEGER NOT NULL,
        explanation TEXT NOT NULL,
        sci_fi_fact TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        is_correct INTEGER NOT NULL,
        xp_earned INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES quiz_questions(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mission_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        mission_key TEXT NOT NULL,
        stage INTEGER DEFAULT 1,
        completed INTEGER DEFAULT 0,
        score INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, mission_key),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        sender TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_title TEXT NOT NULL,
        item_url TEXT NOT NULL,
        category TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, item_url),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    seed_quiz_questions(cursor, conn)
    conn.close()

def get_or_create_user(name: str = "AstroCadete", avatar: str = "🚀") -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    row = cursor.fetchone()
    
    if not row:
        cursor.execute("INSERT INTO users (name, avatar, xp, level) VALUES (?, ?, 0, 1)", (name, avatar))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        unlock_badge(user_id, "first_login")
    else:
        cursor.execute("UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE id = ?", (row["id"],))
        conn.commit()
        
    user_dict = dict(row)
    conn.close()
    return user_dict

def update_user_profile(user_id: int, name: str, avatar: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, avatar = ? WHERE id = ?", (name, avatar, user_id))
    conn.commit()
    conn.close()

def add_xp(user_id: int, xp_amount: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (xp_amount, user_id))
    conn.commit()
    cursor.execute("SELECT xp FROM users WHERE id = ?", (user_id,))
    new_xp = cursor.fetchone()["xp"]
    conn.close()
    return new_xp

def unlock_badge(user_id: int, badge_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user_badges (user_id, badge_id) VALUES (?, ?)", (user_id, badge_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def get_user_badges(user_id: int) -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT badge_id FROM user_badges WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [r["badge_id"] for r in rows]

def get_quiz_questions(pillar: Optional[str] = None, difficulty: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM quiz_questions WHERE 1=1"
    params = []
    
    if pillar and pillar != "Todos":
        query += " AND pillar = ?"
        params.append(pillar)
    if difficulty and difficulty != "Todos":
        query += " AND difficulty = ?"
        params.append(difficulty)
        
    query += " ORDER BY RANDOM() LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    results = []
    for r in rows:
        d = dict(r)
        d["options"] = json.loads(d["options_json"])
        results.append(d)
        
    conn.close()
    return results

def record_quiz_attempt(user_id: int, question_id: int, is_correct: bool, xp_earned: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quiz_attempts (user_id, question_id, is_correct, xp_earned) VALUES (?, ?, ?, ?)",
        (user_id, question_id, 1 if is_correct else 0, xp_earned)
    )
    conn.commit()
    conn.close()
    if xp_earned > 0:
        add_xp(user_id, xp_earned)

def get_user_stats(user_id: int) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total, SUM(is_correct) as correct, SUM(xp_earned) as total_quiz_xp FROM quiz_attempts WHERE user_id = ?", (user_id,))
    quiz_stat = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) as badge_count FROM user_badges WHERE user_id = ?", (user_id,))
    badge_stat = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) as completed_missions FROM mission_progress WHERE user_id = ? AND completed = 1", (user_id,))
    mission_stat = cursor.fetchone()
    
    conn.close()
    total_q = quiz_stat["total"] or 0
    correct_q = quiz_stat["correct"] or 0
    return {
        "quizzes_played": total_q,
        "quizzes_correct": correct_q,
        "quiz_accuracy": round((correct_q / total_q * 100), 1) if total_q > 0 else 0,
        "badges_count": badge_stat["badge_count"] or 0,
        "completed_missions": mission_stat["completed_missions"] or 0
    }

def save_mission_progress(user_id: int, mission_key: str, stage: int, completed: bool, score: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mission_progress (user_id, mission_key, stage, completed, score, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id, mission_key) DO UPDATE SET
            stage = excluded.stage,
            completed = excluded.completed,
            score = MAX(mission_progress.score, excluded.score),
            updated_at = CURRENT_TIMESTAMP
    """, (user_id, mission_key, stage, 1 if completed else 0, score))
    conn.commit()
    conn.close()

def get_mission_progress(user_id: int, mission_key: str) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mission_progress WHERE user_id = ? AND mission_key = ?", (user_id, mission_key))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {"stage": 1, "completed": 0, "score": 0}

def save_chat_message(user_id: int, sender: str, message: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, sender, message) VALUES (?, ?, ?)", (user_id, sender, message))
    conn.commit()
    conn.close()

def get_chat_history(user_id: int, limit: int = 20) -> List[Dict[str, str]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sender, message FROM chat_history WHERE user_id = ? ORDER BY id ASC LIMIT ?", (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r["sender"], "content": r["message"]} for r in rows]

def seed_quiz_questions(cursor, conn):
    cursor.execute("SELECT COUNT(*) FROM quiz_questions")
    if cursor.fetchone()[0] > 0:
        return
        
    questions = [
        # --- FÍSICA ---
        {
            "pillar": "Física",
            "category": "Gravidade",
            "difficulty": "Cadete",
            "question": "Se você pular na Lua, você sobe muito mais alto do que na Terra. Por que isso acontece?",
            "options": [
                "A Lua não tem chão sólido",
                "A gravidade da Lua é cerca de 6 vezes menor que a da Terra porque ela tem menos massa",
                "Na Lua você perde toda a sua massa corporal",
                "O traje de astronauta tem molas especiais nos pés"
            ],
            "correct_idx": 1,
            "explanation": "A força da gravidade depende da massa do corpo celeste. Como a Lua tem cerca de 1% da massa da Terra, sua atração gravitacional é 1/6 da terrestre!",
            "sci_fi_fact": "Em Perdido em Marte, a gravidade é 38% da Terra, o que torna carregar equipamentos pesados bem mais fácil!"
        },
        {
            "pillar": "Física",
            "category": "Relatividade",
            "difficulty": "Mestre",
            "question": "No filme Interestelar, por que 1 hora no Planeta de Miller equivale a 7 anos na Terra?",
            "options": [
                "Porque o planeta gira muito rápido em torno do seu próprio eixo",
                "Devido à extrema dilatação gravitacional do tempo causada pelo buraco negro gigante Gargantua",
                "Porque a atmosfera de água altera a velocidade da luz",
                "É apenas um erro de cálculo do computador TARS"
            ],
            "correct_idx": 1,
            "explanation": "A Teoria da Relatividade Geral de Albert Einstein provou que quanto mais forte o campo gravitacional, mais devagar o tempo passa para quem está nele!",
            "sci_fi_fact": "Kip Thorne, físico ganhador do Prêmio Nobel, fez os cálculos matemáticos exatos para o filme Interestelar!"
        },
        {
            "pillar": "Física",
            "category": "Gravidade Artificial",
            "difficulty": "Cientista",
            "question": "Em Devoradores de Estrelas e em estações espaciais circulares, como os cientistas criam gravidade artificial?",
            "options": [
                "Usando ímãs gigantes no chão da nave",
                "Girando a nave em torno de um eixo central para gerar força centrífuga",
                "Injetando oxigênio pressurizado",
                "Usando matéria escura concentrada no casco"
            ],
            "correct_idx": 1,
            "explanation": "A rotação gera uma aceleração centrípeta (que nós sentimos como força centrífuga contra o chão), empurrando os astronautas contra a parede interna!",
            "sci_fi_fact": "Na nave Hail Mary, Ryland Grace ajusta a rotação para simular exatamente 1g (a gravidade normal da Terra)."
        },
        {
            "pillar": "Física",
            "category": "Velocidade de Escape",
            "difficulty": "Cientista",
            "question": "O que é Velocidade de Escape para um foguete?",
            "options": [
                "A velocidade necessária para escapar do trânsito na base de lançamento",
                "A velocidade mínima para um objeto se libertar da atração gravitacional de um planeta sem cair de volta",
                "A velocidade máxima que um motor a diesel consegue atingir",
                "A velocidade da luz quando viaja no vácuo"
            ],
            "correct_idx": 1,
            "explanation": "Na Terra, a velocidade de escape é cerca de 11,2 km/s (mais de 40.000 km/h). Em Marte, por ser menor, é apenas 5 km/s!",
            "sci_fi_fact": "No livro Perdido em Marte, Mark Watney teve que retirar o escudo e partes do MAV para deixá-lo leve o suficiente para atingir a velocidade de escape!"
        },

        # --- MATEMÁTICA ---
        {
            "pillar": "Matemática",
            "category": "Notação Científica",
            "difficulty": "Cadete",
            "question": "A distância média da Terra ao Sol é de aproximadamente 150.000.000 km. Como escrevemos esse número em Notação Científica?",
            "options": [
                "15 x 10^7 km",
                "1,5 x 10^8 km",
                "1,5 x 10^6 km",
                "150 x 10^6 km"
            ],
            "correct_idx": 1,
            "explanation": "Na notação científica, o número principal deve estar entre 1 e 10. Andamos a vírgula 8 casas para a esquerda: 1,5 × 10⁸ km!",
            "sci_fi_fact": "Os astrônomos usam potências de 10 para medir o cosmos porque escrever zeros demais ocuparia páginas inteiras!"
        },
        {
            "pillar": "Matemática",
            "category": "Anos-Luz",
            "difficulty": "Cientista",
            "question": "A luz viaja a cerca de 300.000 km/s. Se 1 ano tem cerca de 31.500.000 segundos, aproximadamente quanto mede 1 Ano-Luz?",
            "options": [
                "Cerca de 9,46 trilhões de quilômetros (9,46 x 10^12 km)",
                "Cerca de 300 mil quilômetros",
                "Exatamente 1 bilhão de quilômetros",
                "365 mil quilômetros"
            ],
            "correct_idx": 0,
            "explanation": "Distância = Velocidade × Tempo. Multiplicando 300.000 km/s por 31.536.000 s obtemos aproximadamente 9.460.000.000.000 km!",
            "sci_fi_fact": "A estrela mais próxima de nós depois do Sol (Próxima Centauri) fica a 4,24 anos-luz de distância."
        },
        {
            "pillar": "Matemática",
            "category": "Proporção & Tempo",
            "difficulty": "Cadete",
            "question": "Um Sol marciano dura 24 horas e 39 minutos. Se Mark Watney sobreviveu 100 Sols em Marte, isso equivale a:",
            "options": [
                "Exatamente 100 dias terrestres",
                "Aproximadamente 102 dias e 17 horas terrestres",
                "50 dias terrestres",
                "200 dias terrestres"
            ],
            "correct_idx": 1,
            "explanation": "Como cada Sol tem 39 minutos a mais que um dia na Terra, 100 Sols acumulam 3.900 minutos extras (65 horas, ou quase 2,7 dias extras)!",
            "sci_fi_fact": "Os engenheiros da NASA que operam os robôs Curiosity e Perseverance ajustam seus relógios de pulso para o tempo de Marte!"
        },

        # --- QUÍMICA ---
        {
            "pillar": "Química",
            "category": "Produção de Água",
            "difficulty": "Cientista",
            "question": "Em Perdido em Marte, como Mark Watney conseguiu fabricar água líquida para suas plantações?",
            "options": [
                "Derretendo cometas que caíram perto do habitat",
                "Decompondo combustível de hidrazina (N2H4) em Hidrogênio (H2) e reagindo com Oxigênio (O2)",
                "Filtrando a poeira vermelha marciana com café",
                "Condensando vapor do ar marciano que é rico em umidade"
            ],
            "correct_idx": 1,
            "explanation": "A reação clássica de formação de água é 2H₂ + O₂ → 2H₂O. Queimar hidrogênio com oxigênio produz água pura (embora seja uma reação explosiva e perigosa)!",
            "sci_fi_fact": "Mark Watney calculou a estequiometria química com extrema precisão para não explodir a base inteira!"
        },
        {
            "pillar": "Química",
            "category": "Fusão Estelar",
            "difficulty": "Cadete",
            "question": "Qual reação química/nuclear faz o nosso Sol brilhar e gerar tanta energia?",
            "options": [
                "Queima contínua de carvão e petróleo espacial",
                "Fusão nuclear: átomos de Hidrogênio se fundem para formar Hélio",
                "Explosões contínuas de dinamite no núcleo",
                "Oxidação de ferro com vapor d'água"
            ],
            "correct_idx": 1,
            "explanation": "No núcleo das estrelas, temperaturas de mais de 15 milhões de graus fundem 4 prótons de Hidrogênio em 1 núcleo de Hélio, liberando energia pura segundo E = mc²!",
            "sci_fi_fact": "Em Devoradores de Estrelas, os microrganismos chamados Astrofagos absorvem a luz do Sol através de energia de massa enriquecida!"
        },
        {
            "pillar": "Química",
            "category": "Origem dos Elementos",
            "difficulty": "Mestre",
            "question": "De onde vieram o ferro do nosso sangue, o cálcio dos nossos ossos e o ouro das joias?",
            "options": [
                "Foram criados no laboratório do Big Bang e nunca mais mudaram",
                "Foram forjados no interior de estrelas massivas e espalhados pelo universo em explosões de Supernovas",
                "Surgiram espontaneamente no solo dos planetas rochosos",
                "Vieram da atmosfera de Júpiter"
            ],
            "correct_idx": 1,
            "explanation": "Como dizia Carl Sagan: Somos todos poeira de estrelas. Todos os elementos químicos mais pesados que o hélio foram cozidos no núcleo de estrelas que explodiram!",
            "sci_fi_fact": "O amigo alienígena Rocky em Devoradores de Estrelas tem sangue baseado em mercúrio e exoesqueleto de xenonite!"
        },

        # --- TECNOLOGIA COMPUTACIONAL ---
        {
            "pillar": "Computação",
            "category": "Código Hexadecimal",
            "difficulty": "Cientista",
            "question": "Em Perdido em Marte, como Mark Watney conseguiu conversar com a NASA usando a câmera da Pathfinder que só girava 360 graus?",
            "options": [
                "Ele colocou as 26 letras do alfabeto ao redor da sonda com ângulos muito pequenos",
                "Ele usou o sistema Hexadecimal (0 a 9 e A a F), dividindo o círculo em 16 posições de 22,5 graus",
                "Ele usou sinais de fumaça digital",
                "Ele programou um aplicativo de WhatsApp para a sonda"
            ],
            "correct_idx": 1,
            "explanation": "Com 26 letras + números, o espaçamento angular era de apenas 10 graus (muito fácil de errar a leitura). Com Hexadecimal (16 caracteres), cada letra da tabela ASCII era enviada em 2 dígitos perfeitos!",
            "sci_fi_fact": "A tabela ASCII codifica letras como A = 41 (Hex) e M = 4D (Hex). Ciência da computação salvando vidas!"
        },
        {
            "pillar": "Computação",
            "category": "Binário & Radiação",
            "difficulty": "Cadete",
            "question": "Computadores espaciais operam usando o sistema binário (0s e 1s). Por que a memória de computadores no espaço precisa de blindagem especial (Rad-Hard)?",
            "options": [
                "Para não esquentar com a bateria",
                "Porque raios cósmicos e radiação espacial podem inverter bits na memória (Bit-flip) e causar erros críticos",
                "Para impedir que alienígenas instalem vírus",
                "Porque o vácuo apaga arquivos salvos no disco"
            ],
            "correct_idx": 1,
            "explanation": "Partículas de alta energia do Sol e do espaço podem atravessar chips de silício e mudar um bit 0 para 1. Computadores espaciais usam redundância tripla para checagem!",
            "sci_fi_fact": "A sonda Voyager 1 tem 3 computadores idênticos que votam entre si para garantir que nenhum comando seja executado errado!"
        },
        {
            "pillar": "Computação",
            "category": "Robôs e Algoritmos",
            "difficulty": "Mestre",
            "question": "Por que o Rover Perseverance precisa de algoritmos de direção autônoma (AutoNav) em vez de ser controlado com um joystick ao vivo da Terra?",
            "options": [
                "Porque os astronautas na Terra dormem durante a noite de Marte",
                "Porque o sinal de rádio da Terra leva entre 4 e 24 minutos para chegar a Marte, tornando impossível reagir a tempo de evitar um obstáculo",
                "Porque joysticks não funcionam com satélites",
                "Porque o rover se recusa a receber comandos humanos"
            ],
            "correct_idx": 1,
            "explanation": "Devido à velocidade finita da luz (300.000 km/s) e à distância de até 400 milhões de km, a latência de comunicação é de até 20 minutos só de ida!",
            "sci_fi_fact": "O robô TARS em Interestelar possuía parâmetros de inteligência ajustáveis, como 90% de honestidade e 75% de senso de humor!"
        }
    ]
    
    for q in questions:
        cursor.execute("""
            INSERT INTO quiz_questions (pillar, category, difficulty, question, options_json, correct_idx, explanation, sci_fi_fact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            q["pillar"],
            q["category"],
            q["difficulty"],
            q["question"],
            json.dumps(q["options"], ensure_ascii=False),
            q["correct_idx"],
            q["explanation"],
            q.get("sci_fi_fact", "")
        ))
    conn.commit()

if __name__ == "__main__":
    init_db()
    print("Banco de dados Nova Stellaris inicializado com sucesso!")
