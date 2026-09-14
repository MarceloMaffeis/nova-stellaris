"""
Nova Stellaris - Banco de Dados SQLite
Gerenciamento de autenticação, perfis (Alunos & Docentes), progresso, XP, 
insígnias, avisos de sala de aula e perguntas STEAM.
"""

import sqlite3
import json
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nova_stellaris.db")
SECRET_SALT = "NovaStellaris_CosmicSecret_2026"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Gera hash SHA-256 seguro com Salt."""
    return hashlib.sha256(f"{SECRET_SALT}_{password}".encode("utf-8")).hexdigest()

def verify_password(password: str, stored_hash: str) -> bool:
    """Verifica se a senha coincide com o hash gravado."""
    return hash_password(password) == stored_hash

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Tabela de Usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        email TEXT DEFAULT '',
        password_hash TEXT DEFAULT '',
        role TEXT DEFAULT 'aluno',
        class_name TEXT DEFAULT '6º Ano A',
        avatar TEXT DEFAULT '👩‍🚀',
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Migração de Colunas Existentes caso a tabela já tenha sido criada sem elas
    cursor.execute("PRAGMA table_info(users)")
    existing_cols = [row["name"] for row in cursor.fetchall()]
    
    if "email" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT DEFAULT ''")
    if "password_hash" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT DEFAULT ''")
    if "role" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'aluno'")
    if "class_name" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN class_name TEXT DEFAULT '6º Ano A'")
        
    # 2. Tabela de Insígnias
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
    
    # 3. Tabela de Perguntas do Quiz
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
    
    # 4. Tabela de Tentativas do Quiz
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
    
    # 5. Tabela de Progresso em Missões
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
    
    # 6. Tabela de Histórico do Chat com CosmoAI
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
    
    # 7. Tabela de Favoritos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_type TEXT NOT NULL,
        item_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, item_type, item_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
    # 8. Tabela de Avisos & Desafios da Sala de Aula (Mural do Professor)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classroom_announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        teacher_name TEXT NOT NULL,
        class_name TEXT DEFAULT 'Todas as Turmas',
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        xp_reward INTEGER DEFAULT 50,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    
    # Inicializar dados padrão se necessário
    _seed_default_users(cursor, conn)
    _seed_default_questions(cursor, conn)
    _seed_default_announcements(cursor, conn)
    
    conn.close()

def _seed_default_users(cursor, conn):
    """Cria usuários padrão de demonstração para Aluno e Docente."""
    # 1. Aluno Demo (Cadete Estelar)
    cursor.execute("SELECT id FROM users WHERE name = ?", ("Cadete Estelar",))
    if not cursor.fetchone():
        pwd = hash_password("123456")
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, role, class_name, avatar, xp, level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("Cadete Estelar", "cadete@novastellaris.edu", pwd, "aluno", "6º Ano A", "👩‍🚀", 120, 1))
        
    # 2. Docente Demo (Professor Newton)
    cursor.execute("SELECT id FROM users WHERE name = ?", ("Prof. Isaac Newton",))
    if not cursor.fetchone():
        pwd = hash_password("admin123")
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, role, class_name, avatar, xp, level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("Prof. Isaac Newton", "professor@novastellaris.edu", pwd, "docente", "Docente Geral", "👨‍🏫", 9999, 10))
        
    conn.commit()

def _seed_default_announcements(cursor, conn):
    """Cria aviso inicial no mural da turma."""
    cursor.execute("SELECT COUNT(*) as count FROM classroom_announcements")
    if cursor.fetchone()["count"] == 0:
        cursor.execute("""
            INSERT INTO classroom_announcements (teacher_id, teacher_name, class_name, title, content, xp_reward)
            VALUES (
                1, 
                'Prof. Isaac Newton', 
                'Todas as Turmas', 
                '🚀 Boas-vindas à Missão do 6º Ano: Explorando o Sistema Solar!', 
                'Olá Cadetes! Sejam bem-vindos à nossa Estação Nova Stellaris. Sua primeira tarefa é completar o Nível 1 da Trilha de Matemática e da Trilha de Física.', 
                100
            )
        """)
        conn.commit()

def _seed_default_questions(cursor, conn):
    """Popula banco com banco rico de perguntas se estiver vazio."""
    cursor.execute("SELECT COUNT(*) as count FROM quiz_questions")
    if cursor.fetchone()["count"] > 0:
        return
        
    # Inserção das perguntas padrão
    default_questions = [
        ("Física", "Gravidade", "Fácil", "O que aconteceria com o seu peso se você viajasse para a Lua?", json.dumps(["Seu peso aumentaria 6 vezes", "Seu peso diminuiria para cerca de 1/6 do valor na Terra", "Seu peso continuaria exatamente igual", "Você ficaria sem massa"]), 1, "A gravidade na superfície da Lua é de apenas 1,62 m/s² (cerca de 1/6 da gravidade terrestre de 9,81 m/s²), logo sua força peso diminui!", "Os astronautas das missões Apollo saltitavam na Lua com facilidade carregando trajes pesados de 80 kg."),
        ("Matemática", "Escala", "Fácil", "Se 1 Unidade Astronômica (1 UA) é a distância da Terra ao Sol (~150 milhões de km), quanto vale 2 UA?", json.dumps(["75 milhões de km", "300 milhões de km", "450 milhões de km", "1 bilhão de km"]), 1, "Basta multiplicar: 2 x 150.000.000 km = 300.000.000 km.", "Marte orbita a aproximadamente 1,5 UA do Sol."),
        ("Química", "Forja Estelar", "Fácil", "Qual é o elemento químico mais leve e abundante no Universo e no Sol?", json.dumps(["Hélio (He)", "Hidrogênio (H)", "Oxigênio (O)", "Ferro (Fe)"]), 1, "O Hidrogênio (H) é o elemento número 1 da tabela periódica e compõe mais de 73% da matéria observável do Cosmos.", "No Sol, o hidrogênio se funde gerando hélio sob temperaturas de 15 milhões de graus!"),
        ("Tecnologia", "Computação", "Fácil", "Qual é o sistema numérico básico utilizado pelos computadores e sondas espaciais, composto apenas por 0 e 1?", json.dumps(["Sistema Decimal", "Sistema Romano", "Sistema Binário", "Sistema Hexadecimal"]), 2, "O sistema binário (base 2) usa os dígitos 0 e 1, correspondendo a estados desligado/ligado nos circuitos eletrônicos.", "A sonda Voyager 1 transmite dados binários através de ondas de rádio a mais de 24 bilhões de km da Terra.")
    ]
    
    cursor.executemany("""
        INSERT INTO quiz_questions (pillar, category, difficulty, question, options_json, correct_idx, explanation, sci_fi_fact)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, default_questions)
    conn.commit()


# ==============================================================================
# AUTENTICAÇÃO & GESTÃO DE USUÁRIOS
# ==============================================================================
def register_user(name: str, password: str, role: str = "aluno", avatar: str = "👩‍🚀", class_name: str = "6º Ano A", email: str = "") -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Registra um novo usuário com senha criptografada."""
    name = name.strip()
    if not name:
        return False, "O nome de usuário não pode estar em branco.", None
    if len(password) < 4:
        return False, "A senha deve conter pelo menos 4 caracteres.", None
        
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        pwd_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, role, class_name, avatar, xp, level)
            VALUES (?, ?, ?, ?, ?, ?, 0, 1)
        """, (name, email.strip(), pwd_hash, role, class_name, avatar))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_dict = dict(cursor.fetchone())
        conn.close()
        return True, "Cadastro realizado com sucesso!", user_dict
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Já existe um usuário cadastrado com esse nome. Escolha outro nome ou faça login.", None
    except Exception as e:
        conn.close()
        return False, f"Erro ao cadastrar: {str(e)}", None

def authenticate_user(login_identifier: str, password: str) -> Optional[Dict[str, Any]]:
    """Autentica por nome de usuário ou email."""
    login_identifier = login_identifier.strip()
    if not login_identifier or not password:
        return None
        
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM users 
        WHERE name = ? OR (email != '' AND email = ?)
    """, (login_identifier, login_identifier))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return None
        
    user = dict(row)
    # Se o usuário não tem senha cadastrada (antigo), aceita qualquer senha e salva o hash
    if not user.get("password_hash"):
        new_hash = hash_password(password)
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user["id"]))
        conn.commit()
        conn.close()
        return user
        
    if verify_password(password, user["password_hash"]):
        cursor.execute("UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE id = ?", (user["id"],))
        conn.commit()
        conn.close()
        return user
        
    conn.close()
    return None

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_or_create_user(name: str = "Cadete Estelar", avatar: str = "👩‍🚀") -> Dict[str, Any]:
    """Mantém compatibilidade com sessões legadas."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        user_dict = dict(row)
        conn.close()
        return user_dict
    
    pwd_hash = hash_password("123456")
    cursor.execute("""
        INSERT INTO users (name, password_hash, role, class_name, avatar, xp, level)
        VALUES (?, ?, 'aluno', '6º Ano A', ?, 0, 1)
    """, (name, pwd_hash, avatar))
    conn.commit()
    user_id = cursor.lastrowid
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_dict = dict(cursor.fetchone())
    conn.close()
    return user_dict

def update_user_profile(user_id: int, new_name: str, new_avatar: str, new_class: str = None) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if new_class:
            cursor.execute("UPDATE users SET name = ?, avatar = ?, class_name = ? WHERE id = ?", (new_name, new_avatar, new_class, user_id))
        else:
            cursor.execute("UPDATE users SET name = ?, avatar = ? WHERE id = ?", (new_name, new_avatar, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False

def reset_user_password(user_id: int, new_password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        pwd_hash = hash_password(new_password)
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (pwd_hash, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False

def delete_user(user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


# ==============================================================================
# PAINEL DO DOCENTE / GESTÃO DE TURMAS
# ==============================================================================
def get_all_students(class_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if class_filter and class_filter != "Todas as Turmas":
        cursor.execute("""
            SELECT u.*, 
                   COUNT(b.id) as badges_count,
                   COUNT(q.id) as quiz_attempts_count
            FROM users u
            LEFT JOIN user_badges b ON u.id = b.user_id
            LEFT JOIN quiz_attempts q ON u.id = q.user_id
            WHERE u.role = 'aluno' AND u.class_name = ?
            GROUP BY u.id
            ORDER BY u.xp DESC
        """, (class_filter,))
    else:
        cursor.execute("""
            SELECT u.*, 
                   COUNT(b.id) as badges_count,
                   COUNT(q.id) as quiz_attempts_count
            FROM users u
            LEFT JOIN user_badges b ON u.id = b.user_id
            LEFT JOIN quiz_attempts q ON u.id = q.user_id
            WHERE u.role = 'aluno'
            GROUP BY u.id
            ORDER BY u.xp DESC
        """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_classes() -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT class_name FROM users WHERE class_name != '' AND role = 'aluno' ORDER BY class_name")
    rows = cursor.fetchall()
    conn.close()
    classes = [r["class_name"] for r in rows]
    return classes if classes else ["6º Ano A", "6º Ano B", "7º Ano A", "8º Ano A", "9º Ano A", "Clube de Astronomia"]

def get_class_stats(class_filter: Optional[str] = None) -> Dict[str, Any]:
    students = get_all_students(class_filter)
    total_students = len(students)
    if total_students == 0:
        return {
            "total_students": 0,
            "avg_xp": 0,
            "total_xp": 0,
            "total_badges": 0,
            "top_student": "Nenhum"
        }
        
    total_xp = sum(s["xp"] for s in students)
    avg_xp = total_xp / total_students
    total_badges = sum(s["badges_count"] for s in students)
    top_student = students[0]["name"] if students else "Nenhum"
    
    return {
        "total_students": total_students,
        "avg_xp": avg_xp,
        "total_xp": total_xp,
        "total_badges": total_badges,
        "top_student": top_student
    }

def award_bonus_xp(user_id: int, xp_amount: int, reason: str = "Participação em Aula") -> bool:
    """O professor concede XP bônus para um aluno específico."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (xp_amount, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


# ==============================================================================
# MURAL DE AVISOS & MISSÕES DA SALA DE AULA
# ==============================================================================
def create_announcement(teacher_id: int, teacher_name: str, title: str, content: str, class_name: str = "Todas as Turmas", xp_reward: int = 50) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO classroom_announcements (teacher_id, teacher_name, class_name, title, content, xp_reward)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (teacher_id, teacher_name, class_name, title.strip(), content.strip(), xp_reward))
    conn.commit()
    ann_id = cursor.lastrowid
    conn.close()
    return ann_id

def get_announcements(class_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if class_filter and class_filter != "Todas as Turmas":
        cursor.execute("""
            SELECT * FROM classroom_announcements
            WHERE class_name = 'Todas as Turmas' OR class_name = ?
            ORDER BY created_at DESC
        """, (class_filter,))
    else:
        cursor.execute("SELECT * FROM classroom_announcements ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_announcement(ann_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM classroom_announcements WHERE id = ?", (ann_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


# ==============================================================================
# XP & INSÍGNIAS
# ==============================================================================
def add_xp(user_id: int, amount: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET xp = xp + ?, last_active = CURRENT_TIMESTAMP WHERE id = ?", (amount, user_id))
    cursor.execute("SELECT xp FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return row["xp"] if row else 0

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

def get_user_stats(user_id: int) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) as count FROM user_badges WHERE user_id = ?", (user_id,))
    badge_count = cursor.fetchone()["count"]
    cursor.execute("SELECT COUNT(*) as count, COALESCE(SUM(is_correct), 0) as correct FROM quiz_attempts WHERE user_id = ?", (user_id,))
    quiz_row = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) as count FROM mission_progress WHERE user_id = ? AND completed = 1", (user_id,))
    missions_completed = cursor.fetchone()["count"]
    conn.close()
    
    quiz_total = quiz_row["count"] or 0
    quiz_correct = quiz_row["correct"] or 0
    accuracy = round((quiz_correct / quiz_total * 100), 1) if quiz_total > 0 else 0.0
    
    return {
        "user": dict(user_row) if user_row else {},
        "badges_count": badge_count,
        "quiz_total": quiz_total,
        "quiz_correct": quiz_correct,
        "quizzes_played": quiz_total,
        "quizzes_correct": quiz_correct,
        "quiz_accuracy": accuracy,
        "accuracy": accuracy,
        "missions_completed": missions_completed
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

def get_mission_progress(user_id: int, mission_key: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mission_progress WHERE user_id = ? AND mission_key = ?", (user_id, mission_key))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def save_chat_message(user_id: int, sender: str, message: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, sender, message) VALUES (?, ?, ?)", (user_id, sender, message))
    conn.commit()
    conn.close()

def get_chat_history(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sender, message, created_at FROM chat_history WHERE user_id = ? ORDER BY id ASC LIMIT ?", (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["role"] = d.get("sender", "user")
        d["content"] = d.get("message", "")
        result.append(d)
    return result

def clear_chat_history(user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False

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
    conn.close()
    
    questions = []
    for r in rows:
        q = dict(r)
        q["options"] = json.loads(q["options_json"])
        questions.append(q)
    return questions

def save_quiz_attempt(user_id: int, question_id: int, is_correct: bool, xp_earned: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_attempts (user_id, question_id, is_correct, xp_earned)
        VALUES (?, ?, ?, ?)
    """, (user_id, question_id, 1 if is_correct else 0, xp_earned))
    conn.commit()
    conn.close()

# Alias para compatibilidade
record_quiz_attempt = save_quiz_attempt

