# 🪞 Mi Armoire — Image Generation QA Pipeline

A complete eval system for testing and scoring Mi Armoire's image generation quality.

---

## What's In Here

| File | Purpose |
|------|---------|
| `QA_CHECKLIST.md` | Manual review guide — score dimensions explained |
| `test_prompts.py` | 8 fixed test inputs covering edge cases and scenarios |
| `run_eval.py` | Automated eval script — runs prompts, saves images, scores with Claude vision |
| `qa_dashboard.py` | Streamlit QA dashboard — visual side-by-side review UI |
| `eval_results/` | Auto-created on first run — stores JSON results + markdown reports |

---

## Setup

This folder lives **inside** your Mi Armoire project directory:

```
miarmoire/
├── agent.py
├── app.py
├── .env
└── miarmoire-qa/       ← this folder
    ├── run_eval.py
    ├── qa_dashboard.py
    └── ...
```

Install extra dependency:
```powershell
pip install anthropic
```

Add to your `.env` (in the main `miarmoire/` folder):
```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Three Ways to Run QA

### 1. Manual checklist
Open `QA_CHECKLIST.md`, run Mi Armoire normally, score each image yourself.

### 2. Automated eval script
```powershell
# From miarmoire/ with venv active:
cd miarmoire-qa
python run_eval.py                    # runs all 8 tests
python run_eval.py --ids T01 T03     # run specific tests
```
Outputs saved to `eval_results/results_TIMESTAMP.json` and `report_TIMESTAMP.md`.

### 3. QA Dashboard (recommended to show Robert)
```powershell
# From miarmoire/ root:
streamlit run miarmoire-qa/qa_dashboard.py
```
Opens at http://localhost:8502 (or next available port).
Enter your API keys in the sidebar, select tests, click **Run Eval Pipeline**.

---

## Eval Dimensions

| Dimension | What it measures |
|-----------|-----------------|
| Prompt Adherence | Did the image match the garments/colours requested? |
| Visual Quality | Sharpness, no artifacts, no distorted anatomy |
| Fashion Coherence | Does the outfit look like a real styled look? |
| Occasion Fit | Does the image setting match the occasion? |
| Body Awareness | Does the body type reflect the user's height/weight? |

Each scored 1–5 by Claude claude-sonnet-4-20250514 vision. Pass threshold: **≥ 3.5 avg**.

---

## Test Prompt Coverage

| ID | Scenario |
|----|---------|
| T01 | Minimal wardrobe, casual |
| T02 | Full wardrobe, mixed occasions |
| T03 | Evening / formal |
| T04 | Office / smart casual |
| T05 | Colourful, pattern-heavy |
| T06 | Edge case — very short wardrobe |
| T07 | Edge case — no body info |
| T08 | Festival / statement looks |