<!-- Installation de l'environnement -->
conda activate LLM2
pip install -r requirements.txt
pip install litellm
<!-- Configuration d'Ollama -->
ollama pull deepseek-r1:1.5b
<!-- Modes d'Exécution -->
<!-- Option 1 : Mode Console (CLI) -->
cd mon_agent_cv
python -m src.main

<!-- Option 2 : Mode Interface Web (Streamlit) -->
set PYTHONPATH=.
streamlit run src/app.py