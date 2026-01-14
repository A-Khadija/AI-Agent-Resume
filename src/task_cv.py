# src/task_cv.py

from crewai import Task
from .agent_cv import cv_agent, match_agent

# ---------- Tâche 1 : donner la spécialité du CV ----------
def create_cv_task(cv_text: str) -> Task:
    return Task(
        description=(
            "Analyse ce CV :\n\n"
            f"{cv_text}\n\n"
            "Objectif : Donne UNE seule spécialité principale du candidat.\n"
            "Tu dois répondre UNIQUEMENT au format JSON valide :\n"
            "{\n"
            '  \"specialite\": \"...\",\n'
            '  \"justification\": \"...\" \n'
            "}\n"
            "Pas de texte avant ni après le JSON."
        ),
        expected_output="Un JSON avec la spécialité et une justification.",
        agent=cv_agent,
    )

# ---------- Tâche 2 : scoring CV - Offre ----------
def create_matching_task(cv_text: str, job_offer_text: str) -> Task:
    return Task(
        description=(
            "Compare brièvement ce CV et cette offre.\n\n"
            f"CV: {cv_text[:2000]}\n" # On limite le texte envoyé
            f"Offre: {job_offer_text[:2000]}\n"
            "Justification: MAXIMUM 3 phrases." # On force la brièveté
        ),
        expected_output="Un JSON court avec score et justification succincte.",
        agent=match_agent,
)