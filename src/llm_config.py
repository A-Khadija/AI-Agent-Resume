# src/llm_config.py
from crewai import LLM
import os

# Utilisation de DeepSeek-R1 (Modèle de raisonnement ultra-rapide)
llama3_llm = LLM(
    model="ollama/deepseek-r1:1.5b",
    api_base="http://localhost:11434",
    temperature=0.1, # On garde une température basse pour le JSON strict
    timeout=300
)