import json
import streamlit as st
from pypdf import PdfReader
from crewai import Crew

from src.task_cv import create_cv_task, create_matching_task

# =======================
# Helpers
# =======================
def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts).strip()

def read_uploaded_file(uploaded) -> str:
    if uploaded is None:
        return ""
    name = uploaded.name.lower()
    if name.endswith(".txt"):
        return uploaded.read().decode("utf-8", errors="ignore").strip()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded)
    return ""

def parse_json_loose(text: str):
    if not text: return None
    
    # Étape 1 : Retirer les balises de réflexion de DeepSeek si elles existent
    if "<think>" in text:
        text = text.split("</think>")[-1].strip()
        
    # Étape 2 : Nettoyage classique du Markdown
    text = text.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(text)
    except Exception:
        # Étape 3 : Recherche manuelle des accolades
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end + 1])
            except:
                return None
    return None
   

def get_task_raw_output(task) -> str:
    try:
        if hasattr(task, "output") and task.output is not None:
            if hasattr(task.output, "raw") and task.output.raw is not None:
                return str(task.output.raw)
            return str(task.output)
    except Exception:
        pass
    return ""

# =======================
# Page config
# =======================
st.set_page_config(page_title="AI Talent Matcher • CrewAI", page_icon="⚡", layout="wide")

# =======================
# Style (CSS) - Nouveau Thème Midnight Amber
# =======================
st.markdown("""
<style>
/* Fond principal */
.stApp {
    background-color: #050a14;
    color: #e0e6ed;
}

/* Header / Hero */
.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #1d4ed8 100%);
    border-left: 5px solid #fbbf24;
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
}

.hero h1 {
    color: #fbbf24 !important;
    font-weight: 800;
    margin: 0;
}

/* Cartes de contenu */
.card {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease;
}

.card:hover {
    border-color: rgba(251, 191, 36, 0.3);
}

/* Labels et Titres */
.label {
    color: #94a3b8;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* Custom Button */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #fbbf24 0%, #f59e0b 100%);
    color: #050a14;
    border: none;
    font-weight: bold;
    padding: 12px 24px;
    border-radius: 8px;
    width: 100%;
}

div.stButton > button:hover {
    box-shadow: 0 0 15px rgba(251, 191, 36, 0.4);
    transform: translateY(-2px);
}

/* Sidebar / Toggle tweaks */
.stToggle {
    background: #1e293b;
    padding: 10px;
    border-radius: 10px;
}

hr {
    border: none;
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# =======================
# Header
# =======================
st.markdown("""
<div class="hero">
    <h1>⚡ AI Talent Matcher</h1>
    <div style="color: #94a3b8; font-size: 1.1rem;">
        Analyse de CV multi-agents propulsée par <b>CrewAI & Llama 3</b>
    </div>
</div>
""", unsafe_allow_html=True)

# =======================
# Inputs
# =======================
left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="label"> Documents source</div>', unsafe_allow_html=True)
    
    cv_file = st.file_uploader("Déposer le CV (PDF/TXT)", type=["pdf", "txt"])
    st.write("")
    offer_file = st.file_uploader("Déposer l'Offre d'emploi (PDF/TXT)", type=["pdf", "txt"])
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    run = st.button("LANCER L'ANALYSE INTELLIGENTE")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="label">Configuration</div>', unsafe_allow_html=True)
    show_text = st.toggle(" Inspecter le texte extrait", value=False)
    st.info("L'analyse prend généralement 60 à 90 secondes avec Llama 3 en local.")
    st.markdown("</div>", unsafe_allow_html=True)

# =======================
# Run CrewAI
# =======================
if run:
    if not cv_file or not offer_file:
        st.error("Erreur : Veuillez fournir les deux documents.")
        st.stop()

    with st.spinner("⏳ Extraction des données textuelles..."):
        cv_text = read_uploaded_file(cv_file)
        offer_text = read_uploaded_file(offer_file)

    if not cv_text.strip() or not offer_text.strip():
        st.error(" Échec de l'extraction. Assurez-vous que les PDF ne sont pas des images scannées.")
        st.stop()

    if show_text:
        with st.expander("Détails du texte extrait"):
            st.subheader("Texte du CV")
            st.text(cv_text[:1000] + "...")
            st.subheader("Texte de l'Offre")
            st.text(offer_text[:1000] + "...")

    # Création des tâches
    task_specialite = create_cv_task(cv_text)
    task_scoring = create_matching_task(cv_text, offer_text)

    crew = Crew(
        agents=[task_specialite.agent, task_scoring.agent],
        tasks=[task_specialite, task_scoring],
        verbose=True,
    )

    with st.status(" Agents en cours de réflexion...", expanded=True) as status:
        st.write("L'expert analyse le profil...")
        _ = crew.kickoff()
        status.update(label=" Analyse terminée !", state="complete", expanded=False)

    # Récupération
    raw1 = get_task_raw_output(task_specialite)
    raw2 = get_task_raw_output(task_scoring)
    data1 = parse_json_loose(raw1)
    data2 = parse_json_loose(raw2)

    st.write("")
    colA, colB = st.columns(2, gap="medium")

    # Agent 1 - Spécialité
    with colA:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Profil Candidat")
        if data1:
            st.success(f"**Spécialité :** {data1.get('specialite', 'N/A')}")
            st.markdown(f"<p style='color:#94a3b8'>{data1.get('justification', '')}</p>", unsafe_allow_html=True)
        else:
            st.error("Erreur de parsing Agent 1")
            st.code(raw1)
        st.markdown("</div>", unsafe_allow_html=True)

    # Agent 2 - Score
    with colB:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Adéquation Poste")
        if data2:
            score = data2.get('score', 0)
            st.metric("SCORE DE MATCHING", f"{score}%")
            st.progress(int(score) / 100)
            st.markdown(f"<p style='color:#94a3b8'>{data2.get('justification', '')}</p>", unsafe_allow_html=True)
        else:
            st.error("Erreur de parsing Agent 2")
            st.code(raw2)
        st.markdown("</div>", unsafe_allow_html=True)