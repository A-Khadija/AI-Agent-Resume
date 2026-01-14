# src/main.py

import os
from crewai import Crew
from src.task_cv import create_cv_task, create_matching_task

def lire_texte(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    # Dossier racine du projet
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Chemins vers les fichiers
    cv_path = os.path.join(base_dir, "data", "cv1.txt")
    offer_path = os.path.join(base_dir, "data", "offre1.txt")

    # Lire les contenus
    cv_text = lire_texte(cv_path)
    job_offer_text = lire_texte(offer_path)

    # Créer les deux tâches
    task_specialite = create_cv_task(cv_text)
    task_matching = create_matching_task(cv_text, job_offer_text)

    # Construire la Crew multi-agents
    crew = Crew(
        agents=[task_specialite.agent, task_matching.agent],
        tasks=[task_specialite, task_matching],
        verbose=True,
    )

    # Exécuter
    result = crew.kickoff()

    print("\n================= RÉSULTAT GLOBAL =================\n")
    print(result)
    print("\n===================================================\n")