# CV Analyzer (AI Resume Critiquer)

Streamlit app that analyzes PDF/TXT resumes using a local LLM (Ollama + Llama 3).

## Requirements

- Python 3.9+
- Ollama (to run the local model)
- Llama 3 model (via Ollama)

## Setup

1. Clone the repository

2. Create and activate a virtual environment

Windows (PowerShell):

```
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install dependencies

```
pip install streamlit PyPDF2 requests
```

4. Install Ollama and pull the Llama 3 model(you can use another model. It will be better)

- Ollama: https://ollama.com
- Model:

```
ollama pull llama3
```

5. Run the app

```
streamlit run main.py
```

## Usage

- Upload a PDF or TXT resume.
- Enter a target role (optional).
- Click "Analyze Resume".

## Notes

- The app calls Ollama at `http://localhost:11434/api/chat` by default.
- Because the model runs locally, your data is not sent to external services.
