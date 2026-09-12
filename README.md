# 🚀 Nova Stellaris — Universo Interativo STEAM

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?logo=sqlite&logoColor=white)](https://sqlite.org)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-8E75B2.svg?logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Uma plataforma educacional imersiva, gamificada e gratuita criada para jovens de **11 a 13 anos (6º ano do Ensino Fundamental)** e todas as mentes curiosas explorarem a ponte entre o lúdico e a ciência real através dos 4 pilares **STEAM**: **Física, Matemática, Química e Tecnologias Computacionais**.

Inspirado em clássicos modernos da ficção científica rigorosa como ***Devoradores de Estrelas (Project Hail Mary)***, ***Perdido em Marte (The Martian)*** e ***Interestelar (Interstellar)***.

---

## 🌟 O que há dentro da Estação Nova Stellaris?

### 1. 🌌 Observatório do Cosmos & Escala Espacial
- **Atlas Interativo dos Mundos:** Explore planetas rochosos, gigantes gasosos, luas oceânicas (Europa e Encélado) e buracos negros com dados de raio, gravidade, temperatura e conexões com filmes.
- **Balança Planetária:** Descubra seu peso e a altura dos seus pulos em outros mundos através da fórmula da força gravitacional $P = m \cdot g$.
- **Calculadora de Viagem Cósmica:** Compare o tempo de viagem até Marte, Júpiter ou Próxima Centauri na velocidade de caminhada, foguete espacial ($39.000\text{ km/h}$) ou velocidade da luz ($c$).
- **APOD Diário:** Foto astronômica do dia da NASA com explicação traduzida e didática.

### 2. 🚀 Simulador de Missões Sci-Fi (Do Cinema à Realidade)
- 🥔 **Perdido em Marte:** Calcule a proporção química de hidrogênio e oxigênio para produzir água ($2H_2 + O_2 \to 2H_2O$), gerencie o cultivo de batatas para obter calorias suficientes por Sol marciano, e decodifique transmissões em **Hexadecimal da sonda Pathfinder**!
- ✨ **Devoradores de Estrelas:** Ajuste a rotação da nave *Hail Mary* para gerar $1g$ de gravidade artificial por aceleração centrífuga ($a_c = \omega^2 \cdot r$) e comunique-se com o amigável alienígena **Rocky** através de frequências e acordes harmônicos.
- ⏳ **Interestelar (Operação Gargantua):** Calcule a dilatação gravitacional do tempo no Planeta Miller, onde $1\text{ hora} = 7\text{ anos}$ na Terra devido à extrema gravidade do buraco negro!

### 3. 🧮 Laboratório Integrado STEAM
- 🧪 **Química Cósmica:** A Tabela Periódica das Estrelas (de onde vêm os átomos de ferro do seu sangue e cálcio dos seus ossos) e o reator químico de combustíveis de foguetes.
- 💻 **Terminal do Rover:** Mini-IDE para programar rotas autônomas e guiar o Rover Perseverance por labirintos de crateras em Marte.
- 🧮 **Matemática Espacial:** Mago da Notação Científica ($10^x$), potências de 10 e cálculo de volumes planetários ($V = \frac{4}{3}\pi r^3$).
- 🌌 **Física Orbital:** As 3 Leis de Kepler e o Canhão de Newton para entender velocidades de escape e satélites.

### 4. 🤖 CosmoAI — O Mentor Espacial
- Chatbot inteligente com a **Google Gemini API** adotando a persona de um astrofísico empolgante, pronto para responder dúvidas, propor desafios e contar curiosidades com analogias claras.
- Gerador de enigmas espaciais em tempo real com dicas e soluções explicadas.

### 5. 🎮 AstroQuiz STEAM & Gamificação
- Dezenas de desafios categorizados por área (Física, Matemática, Química, Computação) e nível (Cadete, Cientista, Mestre).
- Sistema de **XP, Níveis (de Observador a Mestre Astrofísico Lendário)** e **Galeria de Insígnias Desbloqueáveis** salvas no banco de dados local SQLite.

### 6. 📚 Hub de Conhecimento
- Diretório curado de simuladores 3D online (NASA Eyes, Stellarium 3D, PhET Colorado), canais recomendados do YouTube (Space Today, Ciência Todo Dia, Kurzgesagt Brasil, Manual do Mundo) e guia de obras de ficção científica comentadas.

---

## 💻 Instalação & Execução Rápida

### Pré-requisitos
- Python 3.10 ou superior instalado no computador.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/MarceloMaffeis/nova-stellaris.git
   cd nova-stellaris
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure sua chave da API Gemini (Opcional, chave gratuita já inclusa no template):**
   - Crie um arquivo `.env` ou `.streamlit/secrets.toml`:
     ```toml
     GEMINI_API_KEY = "sua_chave_aqui"
     ```

4. **Inicie o aplicativo:**
   - **No Windows:** Dê um duplo clique no arquivo `run_app.bat` ou execute no PowerShell:
     ```powershell
     streamlit run app.py
     ```
   - O aplicativo abrirá automaticamente no seu navegador em `http://localhost:8501`.

---

## 🗄️ Estrutura do Repositório

```
nova-stellaris/
├── app.py                      # Arquivo principal Streamlit (UI, sidebar, rotas)
├── database.py                 # Gerenciador do SQLite (perfis, XP, quizzes, badges)
├── gemini_service.py           # Serviço de IA do Cosmo (Google Gemini API)
├── requirements.txt            # Dependências Python
├── README.md                   # Documentação do projeto
├── run_app.bat                 # Inicializador 1-clique para Windows
├── run_app.ps1                 # Inicializador PowerShell
├── .streamlit/
│   ├── config.toml             # Configurações do tema escuro cósmico
│   └── secrets.toml            # Chave de API e configurações de segurança
├── assets/
│   ├── styles.css              # CSS do tema espacial glassmorphism
│   └── badges.py               # Definição das insígnias e progressão de ranks
└── modules/
    ├── observatory.py          # Atlas dos Mundos, Balança e APOD da NASA
    ├── sci_fi_missions.py      # Simuladores de Perdido em Marte, Hail Mary e Interestelar
    ├── steam_lab.py            # Laboratório de Física, Matemática, Química e Código
    ├── cosmo_ai.py             # Interface de chat com CosmoAI e enigmas
    ├── quiz_game.py            # AstroQuiz com gamificação e feedback pedagógico
    └── knowledge_hub.py        # Hub com links 3D, canais do YouTube e livros
```

---

## 👨‍🚀 Como Subir para o seu GitHub

Para sincronizar com o seu repositório `MarceloMaffeis/nova-stellaris`:

```bash
git init
git add .
git commit -m "feat: lancamento oficial da estacao espacial Nova Stellaris STEAM"
git branch -M main
git remote add origin https://github.com/MarceloMaffeis/nova-stellaris.git
git push -u origin main
```

---

## 🤝 Licença e Créditos

Distribuído sob a licença **MIT** — livre para todas as crianças, escolas, professores e jovens cientistas que sonham com as estrelas! ✨
