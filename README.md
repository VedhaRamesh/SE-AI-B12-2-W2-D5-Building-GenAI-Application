# Healthy Breakfast AI

A beginner-friendly Streamlit app that uses LangChain and OpenAI to generate
**exactly five** personalized, healthy breakfast ideas. Optional LangSmith
tracing records model runs for observability.

## How it works

- **Streamlit** renders the responsive interface, collects preferences, and
  displays the five ideas.
- **LangChain** builds the role/task/context/example prompt and invokes the
  selected chat model through `langchain-openai`.
- **OpenAI** (`gpt-4o-mini` by default) generates the ideas using the supplied
  diet, cuisine, and priorities.
- **LangSmith** optionally traces LangChain runs when tracing is enabled and a
  LangSmith API key is configured.

The app calls `llm.invoke(prompt)` to synchronously send the formatted prompt
to the model. `invoke()` returns a message object with metadata as well as the
generated answer; the app reads `reply.content` for the text, validates that
it contains exactly five correctly numbered ideas, and shows only those ideas.
It never prints the full message object.

## Project structure

```text
.
├── app.py
├── breakfast.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── tests/
    └── test_breakfast.py
```

## Configure API keys

You need an **OpenAI API key** for generation. A **LangSmith API key** is
optional and is needed only when tracing is enabled.

### Configure environment variables

Copy `.env.example` to `.env` and replace the placeholders with your own keys.
The app loads keys from `.env`; it does not ask for them in the UI. The `.env`
file is ignored by Git:

```dotenv
OPENAI_API_KEY=your-real-openai-key
LANGSMITH_API_KEY=your-real-langsmith-key
LANGSMITH_TRACING=false
LANGSMITH_PROJECT=healthy-breakfast-ai
```

Set `LANGSMITH_TRACING=true` to enable tracing. Supply `LANGSMITH_API_KEY` and,
optionally, a project name in `LANGSMITH_PROJECT`. With tracing disabled, a
LangSmith key is not required. The tracing switch in the app can also enable
or disable tracing for generation.

Never commit `.env`, paste keys into source code, or include keys in screenshots
or terminal output. **Only enter a key into a hosted app if you trust its
operator.** Running locally gives you control over the application code.

## Install and run

Use Python 3.10 or newer.

### macOS / Linux

```bash
cd path/to/SE-AI-B12-2-W2-D5-Building-GenAI-Application
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OpenAI key; LangSmith values are optional unless tracing is enabled.
streamlit run app.py
```

### Windows PowerShell

```powershell
cd path\to\SE-AI-B12-2-W2-D5-Building-GenAI-Application
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and add your OpenAI key; LangSmith values are optional unless tracing is enabled.
streamlit run app.py
```

If PowerShell blocks virtual-environment activation, see Microsoft's execution
policy guidance or use Command Prompt with `.venv\Scripts\activate.bat`.
Alternatively, skip activation and run the environment's Python directly:
`.venv/bin/python -m streamlit run app.py` (macOS/Linux) or
`.venv\Scripts\python.exe -m streamlit run app.py` (Windows).

Open the local URL printed by Streamlit (usually `http://localhost:8501`).
Select diet, cuisine, and priorities in the sidebar, then click
**Generate My 5 Breakfast Ideas**. Click **Clear ideas** to remove the current
results; generate again for a fresh set.

## Test and troubleshoot

Run the local parser tests (no API key or model call is needed):

```bash
python -m unittest discover -s tests -v
```

To verify repeatability, generate twice with the same preferences and compare
the five titles and descriptions. The model is nondeterministic, so consecutive
generations may be different; they can occasionally overlap. A successful
generation is always checked to contain exactly five numbered ideas. The app
uses a non-zero temperature to encourage variety.

Common issues:

- **Missing OpenAI key:** add `OPENAI_API_KEY` to your local `.env` file.
- **Authentication error:** verify the key is valid, active, and permitted to
  use the selected model. The app does not display the key or raw API errors.
- **Quota/rate limit:** check your OpenAI billing and usage limits, then retry.
- **Connection error:** check internet access and retry.
- **LangSmith key required:** tracing is enabled; add `LANGSMITH_API_KEY` to
  your local `.env` file or turn the tracing switch off. Basic generation does not require LangSmith.
- **Invalid model response format:** generate again. The app refuses to render
  a response that does not parse into exactly five items.
- **Import/module error:** activate the virtual environment and install
  `requirements.txt` there.

## Screenshot and GitHub

1. Run the application and generate the five ideas.
2. Capture the app window with the result cards visible. On macOS use
   `Shift-Command-4`; on Windows use Snipping Tool or `Win-Shift-S`; on Linux
   use the desktop screenshot utility.
3. Review the image and ensure it contains no API keys, browser secrets, or
   private account information. Store it as an assignment attachment or add a
   sanitized image such as `screenshots/breakfast-ideas.png`.
4. Before publishing, check `git status --short` and confirm that `.env` is
   absent. The `.gitignore` excludes `.env`, virtual environments, and local
   Streamlit secrets. Never add secrets with force flags.
5. Initialize/select your GitHub repository, then commit and push the source:

```bash
git add app.py breakfast.py requirements.txt .env.example .gitignore README.md tests
git status --short
git commit -m "Build healthy breakfast ideas generator"
git push -u origin main
```

Add a screenshot only after checking it for secrets. Do not add `.env`.

## Assignment checklist

- [x] Streamlit UI with secure key inputs, preferences, loading state, result
  cards, and clear/regenerate actions.
- [x] LangChain `ChatPromptTemplate`, `ChatOpenAI`, and `invoke()` integration.
- [x] Exactly five validated ideas displayed for each successful generation.
- [x] Optional LangSmith tracing and project configuration; no LangSmith key
  needed when tracing is disabled.
- [x] No hard-coded API keys; `.env.example` has placeholders and `.gitignore`
  excludes secrets.
- [x] Friendly handling for missing keys, authentication, quota, network, and
  unexpected errors without displaying secrets.
- [x] Setup, testing, troubleshooting, screenshot, and GitHub publishing
  instructions.
