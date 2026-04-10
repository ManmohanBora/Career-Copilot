import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import re
from pathlib import Path

# ── PAGE CONFIG (must be first Streamlit call) ─────────
st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_PATH = Path(__file__).parent / "database" / "career_copilot.db"

# ── CUSTOM CSS ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Hide default chrome */
#MainMenu, footer{ visibility: hidden; }
[data-testid="stDeployButton"] { display: none; }
[data-testid="stSidebarNav"] { display: none; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060d1a 0%, #0c1a33 100%) !important;
    border-right: 1px solid #1e3a5f;
}

/* Sidebar logo area */
.sidebar-logo {
    text-align: center;
    padding: 20px 10px 28px 10px;
    border-bottom: 1px solid #1e3a5f;
    margin-bottom: 10px;
}
.sidebar-logo h1 {
    font-size: 1.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00d4ff, #0096ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.sidebar-logo p { color: #5a7a9a; font-size: 0.75rem; margin: 4px 0 0 0; }

/* Hero Section */
.hero {
    background: linear-gradient(135deg, #0d2035 0%, #0a3060 50%, #0d2035 100%);
    border: 1px solid #1e4080;
    border-radius: 20px;
    padding: 48px 40px;
    text-align: center;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 50% 50%, rgba(0,150,255,0.06) 0%, transparent 60%);
}
.hero h1 {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #00d4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 12px 0;
    line-height: 1.2;
}
.hero p { color: #7a9cc0; font-size: 1.2rem; margin: 0; }

/* Stat Cards */
.stat-card {
    background: linear-gradient(135deg, #111d30, #0d1a2e);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 28px 20px;
    text-align: center;
    transition: all 0.3s ease;
}
.stat-card:hover {
    border-color: #0096ff;
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,150,255,0.15);
}
.stat-value {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00d4ff, #0096ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.stat-label { color: #5a7a9a; font-size: 0.88rem; margin-top: 8px; text-transform: uppercase; letter-spacing: 0.05em; }

/* Section heading */
.section-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #e0eeff;
    margin: 32px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1e3a5f, transparent);
    margin-left: 12px;
}

/* Cards */
.card {
    background: linear-gradient(135deg, #111d30, #0c1725);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 14px;
    transition: all 0.25s ease;
}
.card:hover {
    border-color: #0096ff55;
    box-shadow: 0 8px 30px rgba(0,100,200,0.12);
}
.card-title { color: #e0eeff; font-size: 1.1rem; font-weight: 600; margin-bottom: 6px; }
.card-sub   { color: #5a7a9a; font-size: 0.88rem; }

/* Job match card */
.job-card {
    background: linear-gradient(135deg, #111d30, #0c1725);
    border: 1px solid #1e3a5f;
    border-left: 4px solid #0096ff;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}
.job-title  { color: #e0eeff; font-size: 1.15rem; font-weight: 700; }
.job-cat    { color: #5a7a9a; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.06em; }
.job-salary { color: #00d4ff; font-size: 1rem; font-weight: 600; margin-top: 6px; }
.match-pct  { font-size: 2rem; font-weight: 800; color: #00ff88; }

/* Skill pills */
.pill {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 50px;
    font-size: 0.80rem;
    margin: 3px;
    font-weight: 500;
}
.pill-blue    { background: rgba(0,150,255,0.15); border: 1px solid rgba(0,150,255,0.4); color: #60b4ff; }
.pill-green   { background: rgba(0,255,136,0.12); border: 1px solid rgba(0,255,136,0.35); color: #00ff88; }
.pill-red     { background: rgba(255,80,60,0.12);  border: 1px solid rgba(255,80,60,0.35);  color: #ff6060; }
.pill-yellow  { background: rgba(255,200,60,0.12); border: 1px solid rgba(255,200,60,0.35); color: #ffd060; }
.pill-purple  { background: rgba(180,120,255,0.12);border: 1px solid rgba(180,120,255,0.35);color: #c090ff; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0070e0, #00b4ff) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 12px 36px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.3s !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0,150,255,0.45) !important;
}

/* Inputs */
.stTextArea textarea, .stSelectbox > div > div, .stMultiSelect > div > div {
    background: #0c1725 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 10px !important;
    color: #e0eeff !important;
}
.stTextArea textarea:focus {
    border-color: #0096ff !important;
    box-shadow: 0 0 0 2px rgba(0,150,255,0.2) !important;
}

/* Progress bar */
.stProgress > div > div > div { background: linear-gradient(90deg, #0096ff, #00d4ff) !important; }

/* Info / Success boxes */
.info-box {
    background: rgba(0,150,255,0.08);
    border: 1px solid rgba(0,150,255,0.3);
    border-radius: 12px;
    padding: 16px 20px;
    color: #80c4ff;
    margin: 12px 0;
}
.success-box {
    background: rgba(0,200,100,0.08);
    border: 1px solid rgba(0,200,100,0.3);
    border-radius: 12px;
    padding: 16px 20px;
    color: #60e8a0;
    margin: 12px 0;
}
.warn-box {
    background: rgba(255,180,0,0.08);
    border: 1px solid rgba(255,180,0,0.3);
    border-radius: 12px;
    padding: 16px 20px;
    color: #ffd060;
    margin: 12px 0;
}

/* Divider */
hr { border-color: #1e3a5f !important; margin: 28px 0 !important; }

/* Radio */
.stRadio > label { color: #7a9cc0 !important; }

/* Expander */
.streamlit-expanderHeader { color: #7ab8ff !important; }
</style>
""", unsafe_allow_html=True)

# ── DATABASE HELPERS ────────────────────────────────────
@st.cache_resource
def get_connection():
    if not DB_PATH.exists():
        st.error("⚠️ Database not found. Run: `python database/setup_db.py` first.")
        st.stop()
    return sqlite3.connect(str(DB_PATH), check_same_thread=False)

def query(sql, params=()):
    conn = get_connection()
    return pd.read_sql_query(sql, conn, params=params)

# ── SKILL EXTRACTION ENGINE ─────────────────────────────
SKILL_ALIASES = {
    "ml": "machine learning", "ai": "artificial intelligence",
    "dl": "deep learning", "cv": "computer vision",
    "nlp": "natural language processing",
    "sklearn": "scikit-learn", "sk-learn": "scikit-learn",
    "powerbi": "power bi", "pbi": "power bi",
    "tf": "tensorflow", "k8s": "kubernetes",
    "gpt": "llm", "gpt-4": "llm", "chatgpt": "llm",
    "langchain": "langchain", "openai": "openai api",
    "hugging face": "huggingface",
}

@st.cache_data
def get_all_skill_names():
    df = query("SELECT name FROM skills")
    return [s.lower() for s in df["name"].tolist()]

def parse_resume(text: str):
    text_lower = text.lower()
    for alias, canonical in SKILL_ALIASES.items():
        text_lower = text_lower.replace(alias, canonical)
    all_skills = get_all_skill_names()
    found = []
    for skill in all_skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return list(set(found))

# ── JOB MATCHING ENGINE ─────────────────────────────────
def match_jobs(user_skills: list):
    df = query("SELECT title, category, required_skills, avg_salary_lpa, demand_score FROM jobs")
    results = []
    user_set = set(s.lower() for s in user_skills)
    for _, row in df.iterrows():
        req = set(json.loads(row["required_skills"]))
        matched = user_set & req
        score = round(len(matched) / len(req) * 100) if req else 0
        results.append({
            "title": row["title"],
            "category": row["category"],
            "salary": row["avg_salary_lpa"],
            "demand": row["demand_score"],
            "match_pct": score,
            "matched_skills": list(matched),
            "missing_skills": list(req - user_set),
            "total_req": len(req),
        })
    return sorted(results, key=lambda x: x["match_pct"], reverse=True)

# ── SKILL GAP ENGINE ────────────────────────────────────
def get_skill_gap(user_skills: list, target_role: str):
    df = query("SELECT required_skills FROM jobs WHERE title = ?", (target_role,))
    if df.empty:
        return [], [], []
    req = set(json.loads(df.iloc[0]["required_skills"]))
    user_set = set(s.lower() for s in user_skills)
    matched = req & user_set
    missing = req - user_set
    return list(matched), list(missing), list(req)

# ═══════════════════════════════════════════════════════
#  PAGE 1 — DASHBOARD
# ═══════════════════════════════════════════════════════
def page_dashboard():
    # Hero
    st.markdown("""
    <div class="hero">
        <h1>🚀 AI Career Copilot</h1>
        <p>Your intelligent guide to navigating the tech job market — powered by real data.</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    total_jobs  = query("SELECT COUNT(*) AS n FROM jobs").iloc[0]["n"]
    total_skills = query("SELECT COUNT(*) AS n FROM skills").iloc[0]["n"]
    total_paths  = query("SELECT COUNT(*) AS n FROM career_paths").iloc[0]["n"]
    total_courses = query("SELECT COUNT(*) AS n FROM courses").iloc[0]["n"]

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label in [
        (c1, total_jobs,   "Job Roles Tracked"),
        (c2, total_skills, "In-Demand Skills"),
        (c3, total_paths,  "Career Paths Mapped"),
        (c4, total_courses,"Learning Resources"),
    ]:
        col.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{val}+</div>
            <div class="stat-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown('<div class="section-title">📈 Top In-Demand Skills</div>', unsafe_allow_html=True)
        df_skills = query("SELECT name, demand_score, category FROM skills ORDER BY demand_score DESC LIMIT 15")
        color_map = {
            "AI/ML": "#0096ff", "Programming": "#00d4ff", "Data": "#00ff88",
            "Visualization": "#a855f7", "Cloud": "#f59e0b", "Math & Stats": "#ef4444",
            "Database": "#ec4899", "Tools": "#14b8a6", "Soft Skills": "#84cc16",
        }
        colors = [color_map.get(c, "#0096ff") for c in df_skills["category"]]
        fig = go.Figure(go.Bar(
            x=df_skills["demand_score"], y=df_skills["name"],
            orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{v}/10" for v in df_skills["demand_score"]],
            textposition="outside", textfont=dict(color="#7ab8ff", size=11),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#7ab8ff", family="Inter"),
            height=440, margin=dict(l=10, r=50, t=10, b=10),
            xaxis=dict(showgrid=False, visible=False, range=[0, 13]),
            yaxis=dict(showgrid=False, color="#7ab8ff", tickfont=dict(size=12)),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">💰 Avg Salary by Category</div>', unsafe_allow_html=True)
        df_sal = query("SELECT category, AVG(avg_salary_lpa) AS avg_sal FROM jobs GROUP BY category ORDER BY avg_sal DESC")
        fig2 = go.Figure(go.Bar(
            x=df_sal["avg_sal"].round(1), y=df_sal["category"],
            orientation="h",
            marker=dict(
                color=df_sal["avg_sal"],
                colorscale=[[0, "#0d2a50"], [0.5, "#0070e0"], [1, "#00d4ff"]],
                line=dict(width=0),
            ),
            text=[f"₹{v:.1f} LPA" for v in df_sal["avg_sal"]],
            textposition="outside", textfont=dict(color="#7ab8ff", size=11),
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#7ab8ff", family="Inter"),
            height=380, margin=dict(l=10, r=80, t=10, b=10),
            xaxis=dict(showgrid=False, visible=False, range=[0, 32]),
            yaxis=dict(showgrid=False, color="#7ab8ff"),
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-title">🔥 Demand by Category</div>', unsafe_allow_html=True)
        df_dem = query("SELECT category, COUNT(*) as n FROM jobs GROUP BY category ORDER BY n DESC")
        fig3 = px.pie(
            df_dem, names="category", values="n", hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig3.update_traces(textfont_size=11, textfont_color="white")
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#7ab8ff", family="Inter"),
            height=300, margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(font=dict(size=10)),
            showlegend=True,
        )
        st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════
#  PAGE 2 — RESUME ANALYZER
# ═══════════════════════════════════════════════════════
def page_resume():
    st.markdown('<h2 style="color:#e0eeff;margin-bottom:4px;">📄 Resume Analyzer</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#5a7a9a;margin-bottom:28px;">Paste your resume or LinkedIn summary. Our AI will extract your skills instantly.</p>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        sample = """Data Scientist with 3 years of experience. Proficient in Python, Pandas, NumPy, Scikit-learn, and TensorFlow. Built deep learning models for image classification using CNN and PyTorch. Experience with SQL, PostgreSQL, and Apache Spark for large-scale data processing. Skilled in data visualization using Matplotlib, Seaborn, and Plotly. Deployed ML models using Docker and AWS. Familiar with Git, Jupyter, and MLflow for experiment tracking. Strong background in statistics and hypothesis testing."""

        resume_text = st.text_area(
            "Paste your resume / LinkedIn about section here:",
            value=st.session_state.get("resume_text", sample),
            height=320,
            placeholder="Paste resume text here...",
            label_visibility="visible",
        )
        analyze_btn = st.button("🔍 Analyze Resume", key="analyze_btn")

    if analyze_btn and resume_text.strip():
        st.session_state["resume_text"] = resume_text
        with st.spinner("Extracting skills..."):
            skills = parse_resume(resume_text)
        st.session_state["user_skills"] = skills

    with col_right:
        user_skills = st.session_state.get("user_skills", [])
        if user_skills:
            df_skills_info = query("SELECT name, category, demand_score FROM skills WHERE name IN ({})".format(
                ",".join(["?"] * len(user_skills))
            ), user_skills)

            st.markdown(f"""
            <div class="success-box">
                ✅ <strong>{len(user_skills)} skills detected</strong> from your resume
            </div>""", unsafe_allow_html=True)

            # Group by category
            category_map = {}
            for _, row in df_skills_info.iterrows():
                category_map.setdefault(row["category"], []).append(row["name"])
            # Add any found skills not in DB metadata
            found_set = set(df_skills_info["name"].tolist())
            uncategorized = [s for s in user_skills if s not in found_set]
            if uncategorized:
                category_map["Other"] = uncategorized

            pill_colors = {
                "AI/ML": "pill-blue", "Programming": "pill-yellow",
                "Data": "pill-green", "Visualization": "pill-purple",
                "Cloud": "pill-yellow", "Math & Stats": "pill-red",
                "Database": "pill-purple", "Tools": "pill-blue",
                "Soft Skills": "pill-green", "Other": "pill-blue",
            }

            for cat, cat_skills in sorted(category_map.items()):
                st.markdown(f'<div style="color:#5a7a9a;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.07em;margin:14px 0 6px 0;">{cat}</div>', unsafe_allow_html=True)
                pill_cls = pill_colors.get(cat, "pill-blue")
                pills = " ".join('<span class="pill ' + pill_cls + '">'+ s +'</span>' for s in cat_skills)
                st.markdown(pills, unsafe_allow_html=True)

            # Skill demand radar
            st.markdown("<br>", unsafe_allow_html=True)
            if not df_skills_info.empty:
                top_skills = df_skills_info.nlargest(8, "demand_score")
                fig = go.Figure(go.Scatterpolar(
                    r=top_skills["demand_score"].tolist() + [top_skills["demand_score"].iloc[0]],
                    theta=top_skills["name"].tolist() + [top_skills["name"].iloc[0]],
                    fill="toself",
                    fillcolor="rgba(0,150,255,0.15)",
                    line=dict(color="#0096ff", width=2),
                    marker=dict(color="#00d4ff", size=7),
                ))
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    polar=dict(
                        bgcolor="rgba(0,0,0,0)",
                        radialaxis=dict(visible=True, range=[0,10], color="#2a4a6a", gridcolor="#1e3a5f"),
                        angularaxis=dict(color="#7ab8ff", gridcolor="#1e3a5f"),
                    ),
                    font=dict(color="#7ab8ff", family="Inter"),
                    height=320, margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div class="info-box">
                💡 Paste your resume on the left and click <strong>Analyze Resume</strong> to get started.
            </div>""", unsafe_allow_html=True)
            # Show sample skill categories
            st.markdown('<div class="section-title" style="margin-top:20px;">🗂️ Skills We Detect</div>', unsafe_allow_html=True)
            cats = query("SELECT category, COUNT(*) as n FROM skills GROUP BY category ORDER BY n DESC")
            for _, row in cats.iterrows():
                st.markdown(f'<span class="pill pill-blue">{row["category"]} · {row["n"]} skills</span>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  PAGE 3 — JOB MATCHER
# ═══════════════════════════════════════════════════════
def page_jobs():
    st.markdown('<h2 style="color:#e0eeff;margin-bottom:4px;">🎯 Job Matcher</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#5a7a9a;margin-bottom:28px;">See which roles best match your current skill profile.</p>', unsafe_allow_html=True)

    user_skills = st.session_state.get("user_skills", [])

    if not user_skills:
        st.markdown("""
        <div class="warn-box">
            ⚠️ No skills detected yet. Go to <strong>Resume Analyzer</strong> first, or add skills manually below.
        </div>""", unsafe_allow_html=True)
        all_skill_names = get_all_skill_names()
        manual = st.multiselect("Or add your skills manually:", options=all_skill_names,
                                 default=["python", "machine learning", "sql", "pandas", "statistics"])
        if manual:
            user_skills = manual
            st.session_state["user_skills"] = manual
    else:
        st.markdown(f"""
        <div class="success-box">
            ✅ Matching against your <strong>{len(user_skills)} detected skills</strong>
        </div>""", unsafe_allow_html=True)

    if not user_skills:
        return

    matches = match_jobs(user_skills)
    top_n = st.slider("Show top N matches:", min_value=3, max_value=15, value=8)
    top_matches = matches[:top_n]

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown('<div class="section-title">🏆 Best Matching Roles</div>', unsafe_allow_html=True)
        for m in top_matches:
            color = "#00ff88" if m["match_pct"] >= 70 else "#ffd060" if m["match_pct"] >= 40 else "#ff6060"
            st.markdown(f"""
            <div class="job-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div class="job-title">{m['title']}</div>
                        <div class="job-cat">{m['category']}</div>
                        <div class="job-salary">₹{m['salary']:.0f} LPA avg  ·  Demand: {'⭐' * (m['demand']//2)}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:2rem;font-weight:800;color:{color};">{m['match_pct']}%</div>
                        <div style="color:#5a7a9a;font-size:0.78rem;">{len(m['matched_skills'])}/{m['total_req']} skills</div>
                    </div>
                </div>
                <div style="margin-top:10px;">
                    {''.join(f'<span class="pill pill-green">{s}</span>' for s in m['matched_skills'][:5])}
                    {''.join(f'<span class="pill pill-red">{s}</span>' for s in m['missing_skills'][:3])}
                </div>
            </div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-title">📊 Match Score Chart</div>', unsafe_allow_html=True)
        titles = [m["title"] for m in top_matches]
        scores = [m["match_pct"] for m in top_matches]
        bar_colors = ["#00ff88" if s >= 70 else "#ffd060" if s >= 40 else "#ff5555" for s in scores]

        fig = go.Figure(go.Bar(
            x=scores, y=titles, orientation="h",
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"{s}%" for s in scores],
            textposition="outside", textfont=dict(color="#7ab8ff", size=11),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#7ab8ff", family="Inter"),
            height=max(350, top_n * 45),
            margin=dict(l=10, r=50, t=10, b=10),
            xaxis=dict(showgrid=False, visible=False, range=[0, 120]),
            yaxis=dict(showgrid=False, color="#7ab8ff", autorange="reversed"),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-title">💼 Salary Potential</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Bar(
            x=[m["salary"] for m in top_matches[:6]],
            y=[m["title"] for m in top_matches[:6]],
            orientation="h",
            marker=dict(
                color=[m["salary"] for m in top_matches[:6]],
                colorscale=[[0,"#0d2a50"],[0.5,"#0070e0"],[1,"#00d4ff"]],
                line=dict(width=0)
            ),
            text=[f"₹{m['salary']:.0f}L" for m in top_matches[:6]],
            textposition="outside", textfont=dict(color="#7ab8ff", size=11),
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#7ab8ff", family="Inter"),
            height=280, margin=dict(l=10, r=60, t=10, b=10),
            xaxis=dict(showgrid=False, visible=False, range=[0, 30]),
            yaxis=dict(showgrid=False, color="#7ab8ff", autorange="reversed"),
        )
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════
#  PAGE 4 — SKILL GAP ANALYZER
# ═══════════════════════════════════════════════════════
def page_gap():
    st.markdown('<h2 style="color:#e0eeff;margin-bottom:4px;">📊 Skill Gap Analyzer</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#5a7a9a;margin-bottom:28px;">Select your dream role and see exactly what skills you need to bridge the gap.</p>', unsafe_allow_html=True)

    user_skills = st.session_state.get("user_skills", [])
    if not user_skills:
        st.markdown("""<div class="warn-box">⚠️ Please analyze your resume first on the <strong>Resume Analyzer</strong> page.</div>""", unsafe_allow_html=True)
        user_skills = ["python", "machine learning", "sql", "pandas", "statistics", "scikit-learn"]

    jobs_list = query("SELECT title FROM jobs ORDER BY title").title.tolist()
    saved_role = st.session_state.get("target_role", "Data Scientist")
    default_idx = jobs_list.index(saved_role) if saved_role in jobs_list else 0

    target_role = st.selectbox("🎯 Select your target role:", jobs_list, index=default_idx)
    st.session_state["target_role"] = target_role

    matched, missing, required = get_skill_gap(user_skills, target_role)
    coverage = round(len(matched) / len(required) * 100) if required else 0

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"""<div class="stat-card"><div class="stat-value" style="color:#00ff88;">{len(matched)}</div><div class="stat-label">Skills You Have</div></div>""", unsafe_allow_html=True)
    col2.markdown(f"""<div class="stat-card"><div class="stat-value" style="color:#ff6060;">{len(missing)}</div><div class="stat-label">Skills to Learn</div></div>""", unsafe_allow_html=True)
    col3.markdown(f"""<div class="stat-card"><div class="stat-value">{coverage}%</div><div class="stat-label">Role Coverage</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(coverage / 100)
    st.markdown(f'<div style="color:#5a7a9a;font-size:0.85rem;text-align:center;margin-top:-8px;">You are <strong style="color:#00d4ff;">{coverage}%</strong> ready for <strong style="color:#e0eeff;">{target_role}</strong></div>', unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown('<div class="section-title">✅ Skills You Have</div>', unsafe_allow_html=True)
        if matched:
            pills = " ".join(f'<span class="pill pill-green">✓ {s}</span>' for s in sorted(matched))
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.markdown('<div class="warn-box">None of the required skills detected yet.</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="margin-top:24px;">❌ Skills to Learn</div>', unsafe_allow_html=True)
        if missing:
            pills = " ".join(f'<span class="pill pill-red">✗ {s}</span>' for s in sorted(missing))
            st.markdown(pills, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">📚 Recommended Courses</div>', unsafe_allow_html=True)
            missing_lower = [m.lower() for m in missing[:5]]
            if missing_lower:
                placeholders = ",".join(["?"] * len(missing_lower))
                df_courses = query(
                    f"SELECT skill_name, course_name, platform, duration, level FROM courses WHERE skill_name IN ({placeholders}) LIMIT 8",
                    missing_lower
                )
                if not df_courses.empty:
                    for _, row in df_courses.iterrows():
                        level_color = {"Beginner": "pill-green", "Intermediate": "pill-yellow", "Advanced": "pill-red"}.get(row["level"], "pill-blue")
                        st.markdown(f"""
                        <div class="card">
                            <div class="card-title">📖 {row['course_name']}</div>
                            <div class="card-sub">
                                {row['platform']} · {row['duration']}
                                <span class="pill {level_color}" style="margin-left:8px;">{row['level']}</span>
                            </div>
                            <div style="margin-top:6px;"><span class="pill pill-purple">🎓 {row['skill_name']}</span></div>
                        </div>""", unsafe_allow_html=True)

    with col_r:
        # Radar chart
        if required:
            radar_skills = list(required)[:9]
            user_set = set(s.lower() for s in user_skills)
            your_scores = [10 if s in user_set else 0 for s in radar_skills]
            required_scores = [10] * len(radar_skills)

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=required_scores + [required_scores[0]],
                theta=radar_skills + [radar_skills[0]],
                fill="toself", name="Required",
                fillcolor="rgba(255,100,60,0.08)",
                line=dict(color="#ff6060", width=1.5, dash="dash"),
            ))
            fig.add_trace(go.Scatterpolar(
                r=your_scores + [your_scores[0]],
                theta=radar_skills + [radar_skills[0]],
                fill="toself", name="Your Skills",
                fillcolor="rgba(0,150,255,0.15)",
                line=dict(color="#0096ff", width=2),
                marker=dict(color="#00d4ff", size=7),
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=False, range=[0, 12]),
                    angularaxis=dict(color="#7ab8ff", gridcolor="#1e3a5f"),
                ),
                font=dict(color="#7ab8ff", family="Inter"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, font=dict(size=11)),
                height=420, margin=dict(l=30, r=30, t=30, b=40),
                title=dict(text=f"Skill Radar: {target_role}", font=dict(color="#7ab8ff", size=13)),
            )
            st.plotly_chart(fig, use_container_width=True)

        # Gap bar chart
        if required:
            statuses = [("✅ " + s, 1) if s in set(s.lower() for s in user_skills) else ("❌ " + s, 0) for s in list(required)[:10]]
            labels = [x[0] for x in statuses]
            values = [x[1] for x in statuses]
            colors = ["#00ff88" if v else "#ff5555" for v in values]
            fig2 = go.Figure(go.Bar(
                y=labels, x=values,
                orientation="h",
                marker=dict(color=colors, line=dict(width=0)),
                text=["Have" if v else "Missing" for v in values],
                textposition="inside", textfont=dict(color="white", size=11),
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#7ab8ff", family="Inter"),
                height=380, margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=False, visible=False, range=[0, 1.3]),
                yaxis=dict(showgrid=False, color="#7ab8ff"),
            )
            st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════
#  PAGE 5 — CAREER PATH
# ═══════════════════════════════════════════════════════
def page_career():
    st.markdown('<h2 style="color:#e0eeff;margin-bottom:4px;">🗺️ Career Path Navigator</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#5a7a9a;margin-bottom:28px;">Discover possible career transitions from your current role.</p>', unsafe_allow_html=True)

    all_roles = query("SELECT DISTINCT from_role FROM career_paths UNION SELECT DISTINCT to_role FROM career_paths ORDER BY from_role").iloc[:,0].tolist()
    saved = st.session_state.get("target_role", "Data Analyst")
    default = all_roles.index(saved) if saved in all_roles else 0

    current_role = st.selectbox("📍 Your current role:", all_roles, index=default)

    df_paths = query("SELECT * FROM career_paths WHERE from_role = ? ORDER BY months_min", (current_role,))

    if df_paths.empty:
        st.markdown(f'<div class="warn-box">No paths found starting from <strong>{current_role}</strong>. Try another role.</div>', unsafe_allow_html=True)
        return

    # Sankey diagram
    all_nodes = [current_role] + df_paths["to_role"].tolist()
    node_idx  = {n: i for i, n in enumerate(all_nodes)}
    src = [node_idx[current_role]] * len(df_paths)
    tgt = [node_idx[r] for r in df_paths["to_role"]]
    diff_color = {"Easy": "rgba(0,200,100,0.6)", "Medium": "rgba(0,150,255,0.6)", "Hard": "rgba(255,80,60,0.6)"}
    link_colors = [diff_color.get(d, "rgba(0,150,255,0.4)") for d in df_paths["difficulty"]]

    fig = go.Figure(go.Sankey(
        arrangement="fixed",
        node=dict(
            pad=20, thickness=28,
            line=dict(color="rgba(0,0,0,0)", width=0),
            label=all_nodes,
            color=["#0096ff"] + ["#1a3a6a"] * len(df_paths["to_role"]),
            x=[0.05] + [0.8] * len(df_paths),
            y=[0.5] + [i / max(len(df_paths) - 1, 1) for i in range(len(df_paths))],
        ),
        link=dict(
            source=src, target=tgt,
            value=[max(1, 12 - row["months_min"]) for _, row in df_paths.iterrows()],
            color=link_colors,
        ),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#7ab8ff", family="Inter", size=13),
        height=380, margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">📋 Transition Details</div>', unsafe_allow_html=True)
    cols = st.columns(min(len(df_paths), 3))
    for i, (_, row) in enumerate(df_paths.iterrows()):
        col = cols[i % len(cols)]
        diff = row["difficulty"]
        diff_pill = {"Easy": "pill-green", "Medium": "pill-yellow", "Hard": "pill-red"}.get(diff, "pill-blue")
        skills = json.loads(row["skills_to_add"])
        with col:
            st.markdown(f"""
            <div class="card">
                <div class="card-title" style="font-size:1.05rem;">➡️ {row['to_role']}</div>
                <div style="margin:8px 0;">
                    <span class="pill {diff_pill}">{diff}</span>
                    <span class="pill pill-blue">⏱ {row['months_min']}–{row['months_max']} months</span>
                </div>
                <div style="color:#5a7a9a;font-size:0.82rem;margin:8px 0 4px 0;">Skills to gain:</div>
                {''.join(f'<span class="pill pill-purple">{s}</span>' for s in skills[:5])}
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  PAGE 6 — INTERVIEW PREP
# ═══════════════════════════════════════════════════════
def page_interview():
    st.markdown('<h2 style="color:#e0eeff;margin-bottom:4px;">💼 Interview Prep</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#5a7a9a;margin-bottom:28px;">Role-specific interview questions curated from real hiring processes.</p>', unsafe_allow_html=True)

    roles_with_q = query("SELECT DISTINCT role FROM interview_questions ORDER BY role").role.tolist()
    saved = st.session_state.get("target_role", "Data Scientist")
    default = roles_with_q.index(saved) if saved in roles_with_q else 0

    col_a, col_b, _ = st.columns([2, 1, 1])
    with col_a:
        selected_role = st.selectbox("🎯 Select role:", roles_with_q, index=default)
    with col_b:
        difficulty = st.selectbox("Difficulty:", ["All", "Easy", "Medium", "Hard"])

    # Fetch questions
    if difficulty == "All":
        df_q = query("SELECT * FROM interview_questions WHERE role IN (?, ?) ORDER BY difficulty, category",
                     (selected_role, "All Roles"))
    else:
        df_q = query("SELECT * FROM interview_questions WHERE role IN (?, ?) AND difficulty = ? ORDER BY category",
                     (selected_role, "All Roles", difficulty))

    if df_q.empty:
        st.markdown('<div class="warn-box">No questions found for this combination.</div>', unsafe_allow_html=True)
        return

    diff_colors = {"Easy": "pill-green", "Medium": "pill-yellow", "Hard": "pill-red"}
    cat_icons   = {"Technical": "⚙️", "Behavioral": "🧠", "Conceptual": "💡", "System Design": "🏗️"}

    # Stats
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="stat-card"><div class="stat-value">{len(df_q)}</div><div class="stat-label">Total Questions</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-card"><div class="stat-value" style="color:#ff6060;">{len(df_q[df_q.difficulty=="Hard"])}</div><div class="stat-label">Hard Questions</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-card"><div class="stat-value" style="color:#ffd060;">{len(df_q[df_q.difficulty=="Medium"])}</div><div class="stat-label">Medium Questions</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    for cat in ["Technical", "System Design", "Conceptual", "Behavioral"]:
        cat_df = df_q[df_q["category"] == cat]
        if cat_df.empty:
            continue
        icon = cat_icons.get(cat, "📌")
        with st.expander(f"{icon} {cat} Questions ({len(cat_df)})", expanded=(cat == "Technical")):
            for i, (_, row) in enumerate(cat_df.iterrows(), 1):
                d_class = diff_colors.get(row["difficulty"], "pill-blue")
                st.markdown(f"""
                <div class="card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px;">
                        <span style="color:#5a7a9a;font-size:0.78rem;">Q{i}</span>
                        <span class="pill {d_class}">{row['difficulty']}</span>
                    </div>
                    <div style="color:#e0eeff;font-size:1rem;line-height:1.5;">{row['question']}</div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  SIDEBAR + MAIN NAVIGATION
# ═══════════════════════════════════════════════════════
def main():
    # Session state defaults
    if "user_skills" not in st.session_state:
        st.session_state["user_skills"] = []
    if "target_role" not in st.session_state:
        st.session_state["target_role"] = "Data Scientist"

    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h1>🚀 AI Career Copilot</h1>
            <p>Powered by Python + SQLite</p>
        </div>""", unsafe_allow_html=True)

        page = st.radio(
            "Navigate",
            ["🏠  Dashboard", "📄  Resume Analyzer", "🎯  Job Matcher",
             "📊  Skill Gap", "🗺️  Career Path", "💼  Interview Prep"],
            label_visibility="collapsed",
        )

        st.markdown("<br><hr>", unsafe_allow_html=True)

        if st.session_state["user_skills"]:
            st.markdown(f"""
            <div class="info-box" style="font-size:0.82rem;">
                🧠 <strong>{len(st.session_state['user_skills'])} skills</strong> in your profile<br>
                🎯 Target: <strong>{st.session_state.get('target_role','—')}</strong>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warn-box" style="font-size:0.82rem;">
                💡 Start by analyzing your resume on the <strong>Resume Analyzer</strong> page.
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style="position:fixed;bottom:20px;color:#2a4a6a;font-size:0.72rem;text-align:center;width:220px;">
            AI Career Copilot © 2025
        </div>""", unsafe_allow_html=True)

    # Route
    if "Dashboard"      in page: page_dashboard()
    elif "Resume"       in page: page_resume()
    elif "Job Matcher"  in page: page_jobs()
    elif "Skill Gap"    in page: page_gap()
    elif "Career Path"  in page: page_career()
    elif "Interview"    in page: page_interview()

if __name__ == "__main__":
    main()
