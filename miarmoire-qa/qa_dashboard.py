"""
Mi Armoire — Image Generation QA Dashboard
A polished eval pipeline UI for running, scoring, and reviewing image gen quality.

Usage:
    streamlit run qa_dashboard.py
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import sys
import json
import time
import datetime
import base64
import glob
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

from test_prompts import TEST_PROMPTS

st.set_page_config(
    page_title="Mi Armoire — QA Dashboard",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'Jost', sans-serif; }
  .stApp { background: #0f0d08; color: #faf6ee; }

  /* Sidebar */
  [data-testid="stSidebar"] { background: #1c1608 !important; border-right: 1px solid rgba(201,168,76,0.2); }
  [data-testid="stSidebar"] * { color: #faf6ee !important; }
  [data-testid="stSidebar"] .stSelectbox > div > div { background: #0f0d08 !important; border: 1px solid #c9a84c !important; }
  [data-testid="stSidebar"] .stTextInput input { background: #0f0d08 !important; border: 1px solid #c9a84c !important; color: #faf6ee !important; }
  [data-testid="stSidebar"] .stMultiSelect > div > div { background: #0f0d08 !important; border: 1px solid rgba(201,168,76,0.4) !important; }

  /* Buttons */
  .stButton > button {
    background: transparent !important;
    color: #c9a84c !important;
    border: 1px solid #c9a84c !important;
    border-radius: 0 !important;
    padding: 0.7rem 1.8rem !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.65rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.3em !important;
    text-transform: uppercase !important;
    transition: all 0.25s !important;
  }
  .stButton > button:hover { background: #c9a84c !important; color: #1c1608 !important; }

  /* Run button primary */
  .run-btn .stButton > button {
    background: #c9a84c !important; color: #1c1608 !important;
    font-weight: 500 !important;
  }

  /* Cards */
  .qa-card {
    background: #1c1608;
    border: 1px solid rgba(201,168,76,0.2);
    padding: 1.5rem;
    margin-bottom: 1.2rem;
  }
  .look-header {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 400;
    color: #faf6ee;
    margin-bottom: 0.2rem;
  }
  .look-meta {
    font-size: 0.62rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #c9a84c;
    margin-bottom: 1rem;
  }
  .score-bar-wrap { margin-bottom: 0.6rem; }
  .score-label {
    font-size: 0.62rem; letter-spacing: 0.2em; text-transform: uppercase;
    color: #8a7a50; margin-bottom: 0.25rem;
  }
  .score-bar-bg {
    background: rgba(201,168,76,0.1);
    height: 6px; width: 100%; position: relative;
  }
  .score-bar-fill {
    height: 6px; background: linear-gradient(90deg, #6b4e1a, #c9a84c, #f5e080);
    transition: width 0.6s ease;
  }
  .score-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem; color: #c9a84c; float: right; margin-top: -1.3rem;
  }
  .pass-badge {
    display: inline-block; padding: 0.2rem 0.8rem;
    font-size: 0.58rem; letter-spacing: 0.2em; text-transform: uppercase;
    font-weight: 500; margin-left: 0.5rem;
  }
  .badge-pass { background: rgba(76,201,120,0.15); color: #4cc978; border: 1px solid #4cc978; }
  .badge-fail { background: rgba(201,76,76,0.15); color: #c94c4c; border: 1px solid #c94c4c; }
  .badge-warn { background: rgba(201,168,76,0.15); color: #c9a84c; border: 1px solid #c9a84c; }
  .badge-na   { background: rgba(100,100,100,0.15); color: #888; border: 1px solid #555; }

  .session-stat {
    background: rgba(201,168,76,0.06);
    border: 1px solid rgba(201,168,76,0.15);
    padding: 1rem 1.5rem;
    text-align: center;
  }
  .stat-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.5rem; color: #c9a84c; line-height: 1;
  }
  .stat-label {
    font-size: 0.58rem; letter-spacing: 0.25em;
    text-transform: uppercase; color: #8a7a50; margin-top: 0.3rem;
  }
  .prompt-box {
    background: #0f0d08; border-left: 2px solid #c9a84c;
    padding: 0.8rem 1rem; font-size: 0.8rem; color: #b8a070;
    font-style: italic; line-height: 1.6; margin-top: 0.8rem;
  }
  .reasoning-box {
    font-size: 0.78rem; color: #8a7a50; font-style: italic;
    line-height: 1.6; margin-top: 0.6rem; padding-top: 0.6rem;
    border-top: 1px solid rgba(201,168,76,0.1);
  }
  .section-title {
    font-size: 0.6rem; letter-spacing: 0.4em; text-transform: uppercase;
    color: #c9a84c; margin-bottom: 1.2rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(201,168,76,0.2);
  }
  .error-box {
    background: rgba(201,76,76,0.1); border: 1px solid rgba(201,76,76,0.3);
    padding: 1rem; color: #c94c4c; font-size: 0.85rem;
  }
  .img-missing {
    background: #1c1608; border: 1px dashed rgba(201,168,76,0.2);
    display: flex; align-items: center; justify-content: center;
    height: 300px; color: #8a7a50;
    font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase;
  }
  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
components.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@200;300;400&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background: #0f0d08; }
.header {
  background: #0f0d08;
  border-bottom: 1px solid rgba(201,168,76,0.25);
  padding: 2rem 3rem 1.5rem;
  display: flex; justify-content: space-between; align-items: flex-end;
}
.title-block .eyebrow {
  font-family: 'Jost', sans-serif; font-weight: 200;
  font-size: 0.58rem; letter-spacing: 0.45em;
  text-transform: uppercase; color: #c9a84c; margin-bottom: 0.5rem;
}
.title-block h1 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.8rem; font-weight: 300; color: #faf6ee; line-height: 1;
}
.title-block h1 em { font-style: italic; }
.title-block h1 span {
  background: linear-gradient(135deg, #6b4e1a, #c9a84c, #f5e080, #c9a84c);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.meta {
  font-family: 'Jost', sans-serif; font-weight: 200;
  font-size: 0.62rem; letter-spacing: 0.25em;
  text-transform: uppercase; color: #8a7a50; text-align: right;
}
</style>
</head>
<body>
<div class="header">
  <div class="title-block">
    <div class="eyebrow">Image Generation QA Pipeline</div>
    <h1><em>Mi</em> <span>Armoire</span> — Eval</h1>
  </div>
  <div class="meta">
    FLUX.1-schnell · LangGraph · Groq<br>
    Claude Vision Scorer
  </div>
</div>
</body>
</html>
""", height=120)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='section-title'>Eval Configuration</div>", unsafe_allow_html=True)

    hf_token = st.text_input("HuggingFace Token", type="password",
                              value=os.environ.get("HF_TOKEN", ""),
                              help="Required for image generation")
    anthropic_key = st.text_input("Anthropic API Key", type="password",
                                  value=os.environ.get("ANTHROPIC_API_KEY", ""),
                                  help="Required for auto-scoring")
    groq_key = st.text_input("Groq API Key", type="password",
                              value=os.environ.get("GROQ_API_KEY", ""),
                              help="Required for the styling agent")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Test Selection</div>", unsafe_allow_html=True)

    test_options = {f"[{t['id']}] {t['label']}": t["id"] for t in TEST_PROMPTS}
    selected_labels = st.multiselect(
        "Select tests to run",
        options=list(test_options.keys()),
        default=list(test_options.keys())[:3],
    )
    selected_ids = [test_options[l] for l in selected_labels]

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Past Results</div>", unsafe_allow_html=True)

    results_dir = os.path.join(os.path.dirname(__file__), "eval_results")
    result_files = sorted(glob.glob(os.path.join(results_dir, "results_*.json")), reverse=True)
    result_labels = ["— Run new eval —"] + [os.path.basename(f) for f in result_files]
    selected_result_file = st.selectbox("Load past results", result_labels)


# ── State ──────────────────────────────────────────────────────────────────────
if "eval_results" not in st.session_state:
    st.session_state.eval_results = None
if "running" not in st.session_state:
    st.session_state.running = False


# ── Load past results ──────────────────────────────────────────────────────────
if selected_result_file != "— Run new eval —" and st.session_state.eval_results is None:
    path = os.path.join(results_dir, selected_result_file)
    with open(path) as f:
        st.session_state.eval_results = json.load(f)


# ── Run button ─────────────────────────────────────────────────────────────────
col_run, col_clear = st.columns([2, 1])

with col_run:
    run_clicked = st.button("▶  Run Eval Pipeline", use_container_width=True)
with col_clear:
    if st.button("Clear Results", use_container_width=True):
        st.session_state.eval_results = None
        st.rerun()

if run_clicked:
    if not selected_ids:
        st.warning("Select at least one test.")
    else:
        # Inject keys into env for this session
        if hf_token:   os.environ["HF_TOKEN"] = hf_token
        if anthropic_key: os.environ["ANTHROPIC_API_KEY"] = anthropic_key
        if groq_key:   os.environ["GROQ_API_KEY"] = groq_key

        # Import eval runner inline
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "run_eval", os.path.join(os.path.dirname(__file__), "run_eval.py")
        )
        eval_mod = importlib.util.load_from_spec = None

        # We'll run inline rather than importing module to avoid reload issues
        from run_eval import run_eval

        progress_text = st.empty()
        progress_bar = st.progress(0)

        results = []
        for i, tid in enumerate(selected_ids):
            progress_text.markdown(
                f"<div style='font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;"
                f"color:#c9a84c'>Running {tid} ({i+1}/{len(selected_ids)})...</div>",
                unsafe_allow_html=True,
            )
            r = run_eval(test_ids=[tid])
            results.extend(r)
            progress_bar.progress((i + 1) / len(selected_ids))

        progress_text.empty()
        progress_bar.empty()
        st.session_state.eval_results = results
        st.rerun()


# ── Results display ────────────────────────────────────────────────────────────
def score_badge(avg):
    if avg is None:
        return "<span class='pass-badge badge-na'>N/A</span>"
    elif avg >= 4.0:
        return "<span class='pass-badge badge-pass'>Pass</span>"
    elif avg >= 3.0:
        return "<span class='pass-badge badge-warn'>Borderline</span>"
    else:
        return "<span class='pass-badge badge-fail'>Fail</span>"


def score_bar(label, score, max_score=5):
    if score is None:
        pct = 0
        display = "—"
    else:
        pct = (score / max_score) * 100
        display = f"{score}/5"
    return f"""
<div class='score-bar-wrap'>
  <div class='score-label'>{label}</div>
  <div class='score-bar-bg'>
    <div class='score-bar-fill' style='width:{pct}%'></div>
  </div>
  <div class='score-num'>{display}</div>
  <div style='clear:both'></div>
</div>
"""


SCORE_LABELS = {
    "prompt_adherence": "Prompt Adherence",
    "visual_quality": "Visual Quality",
    "fashion_coherence": "Fashion Coherence",
    "occasion_fit": "Occasion Fit",
    "body_awareness": "Body Awareness",
}

if st.session_state.eval_results:
    results = st.session_state.eval_results

    # ── Summary stats ──────────────────────────────────────────────────────────
    all_avgs = [r["session_avg"] for r in results if r.get("session_avg")]
    total_looks = sum(len(r.get("looks", [])) for r in results)
    looks_with_images = sum(
        1 for r in results for l in r.get("looks", []) if l.get("image_status") == "ok"
    )

    st.markdown("<div class='section-title'>Session Summary</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    stats = [
        (f"{round(sum(all_avgs)/len(all_avgs), 1)}/5" if all_avgs else "—", "Overall Avg Score"),
        (f"{len(results)}", "Tests Run"),
        (f"{looks_with_images}/{total_looks}", "Images Generated"),
        (f"{sum(1 for a in all_avgs if a >= 3.5)}/{len(all_avgs)}" if all_avgs else "—", "Tests Passed"),
    ]
    for col, (num, label) in zip(cols, stats):
        with col:
            st.markdown(
                f"<div class='session-stat'><div class='stat-num'>{num}</div>"
                f"<div class='stat-label'>{label}</div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Per-test results ───────────────────────────────────────────────────────
    for test in results:
        avg = test.get("session_avg")
        badge = score_badge(avg)

        st.markdown(
            f"<div class='section-title'>"
            f"[{test['id']}] {test['label']}"
            f" {badge}"
            f"<span style='float:right;font-family:Cormorant Garamond,serif;font-size:1rem;color:#c9a84c'>"
            f"Session avg {avg}/5</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        if test.get("error"):
            st.markdown(f"<div class='error-box'>⚠ {test['error']}</div>", unsafe_allow_html=True)
            continue

        for look in test.get("looks", []):
            with st.expander(f"Look {look['look_index']} — {look['outfit_name']}", expanded=True):
                img_col, score_col = st.columns([1, 1])

                with img_col:
                    img_path = look.get("image_path")
                    if img_path and os.path.exists(img_path):
                        st.image(img_path, use_container_width=True)
                    else:
                        status = look.get("image_status", "missing")
                        st.markdown(
                            f"<div class='img-missing'>Image {status}</div>",
                            unsafe_allow_html=True,
                        )
                    st.markdown(
                        f"<div class='prompt-box'>{look.get('image_prompt', '')}</div>",
                        unsafe_allow_html=True,
                    )

                with score_col:
                    st.markdown(
                        f"<div class='look-header'>{look['outfit_name']}</div>"
                        f"<div class='look-meta'>{look.get('occasion', '')} · "
                        f"Jewellery: {look.get('jewellery', 'none')}</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        "**Items:** " + ", ".join(look.get("items", [])),
                    )
                    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

                    scores_html = "".join(
                        score_bar(label, look["scores"].get(dim))
                        for dim, label in SCORE_LABELS.items()
                    )
                    look_avg = look.get("look_avg")
                    avg_badge = score_badge(look_avg)
                    st.markdown(
                        scores_html
                        + f"<div style='margin-top:0.8rem;font-family:Jost,sans-serif;"
                          f"font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:#8a7a50'>"
                          f"Look Avg: <strong style='color:#c9a84c'>{look_avg}/5</strong> {avg_badge}</div>",
                        unsafe_allow_html=True,
                    )

                    if look.get("reasoning"):
                        st.markdown(
                            f"<div class='reasoning-box'>{look['reasoning']}</div>",
                            unsafe_allow_html=True,
                        )

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

else:
    # Empty state
    st.markdown("""
<div style='text-align:center;padding:5rem 0;'>
  <div style='font-family:Cormorant Garamond,serif;font-size:3rem;color:rgba(201,168,76,0.2);margin-bottom:1rem'>🪞</div>
  <div style='font-size:0.65rem;letter-spacing:0.4em;text-transform:uppercase;color:#8a7a50'>
    Select tests on the left and click Run Eval Pipeline
  </div>
</div>
""", unsafe_allow_html=True)