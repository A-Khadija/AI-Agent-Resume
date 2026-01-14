# src/agent_cv.py

from crewai import Agent
from .llm_config import llama3_llm

# ===== Agent 1 : Analyse de CV (spécialité) =====
cv_agent = Agent(
    role="Expert en analyse de CV",
    goal=(
        "Analyser le CV fourni et déterminer UNE seule spécialité principale "
        "du candidat, puis répondre uniquement au format JSON."
    ),
    backstory=(
        "Tu es un expert en classification de profils métiers (Data, IA, Dev, Réseaux, etc.). "
        "Tu dois toujours répondre en français, en JSON strict, sans texte autour."
    ),
    llm=llama3_llm,
    allow_delegation=False,
    verbose=True,
)

# ===== Agent 2 : Matching CV - Offre d'emploi =====
match_agent = Agent(
    role="Expert en matching de profils avec des offres d’emploi",
    goal=(
        "Évaluer l’adéquation entre un CV et une offre d’emploi donnée, "
        "puis produire un score de 0 à 100 avec une justification détaillée, "
        "en JSON strict."
    ),
    backstory=(
        "Tu es un recruteur spécialisé en IA et Data. "
        "Tu compares les compétences, l’expérience et les missions du candidat "
        "avec les besoins de l’offre d’emploi."
    ),
    llm=llama3_llm,
    allow_delegation=False,
    verbose=True,
)