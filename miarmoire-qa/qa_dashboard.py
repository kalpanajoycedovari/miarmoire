"""
Mi Armoire — Image Generation QA Dashboard
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import sys
import json
import glob
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

from test_prompts import TEST_PROMPTS

st.set_page_config(
    page_title="Mi Armoire - QA Dashboard",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap');
  html, body, [class*="css"] { font-family: 'Jost', sans-serif; }
  .stApp { background: #faf6ee; color: #1c1608; }
  [data-testid="stSidebar"] { background: #f0e8d5 !important; border-right: 1px solid rgba(201,168,76,0.3); }
  [data-testid="stSidebar"] * { color: #1c1608 !important; }
  [data-testid="stSidebar"] .stSelectbox > div > div { background: #faf6ee !important; border: 1px solid #c9a84c !important; }
  [data-testid="stSidebar"] .stMultiSelect > div > div { background: #faf6ee !important; border: 1px solid rgba(201,168,76,0.4) !important; }
  [data-testid="stSidebarCollapseButton"] { display: none !important; }
  .stButton > button {
    background: transparent !important; color: #1c1608 !important;
    border: 1px solid #c9a84c !important; border-radius: 0 !important;
    padding: 0.7rem 1.8rem !important; font-family: 'Jost', sans-serif !important;
    font-size: 0.65rem !important; font-weight: 400 !important;
    letter-spacing: 0.3em !important; text-transform: uppercase !important;
    transition: all 0.25s !important;
  }
  .stButton > button:hover { background: #c9a84c !important; color: #1c1608 !important; }
  .look-header { font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; font-weight: 400; color: #1c1608; margin-bottom: 0.2rem; }
  .look-meta { font-size: 0.62rem; letter-spacing: 0.25em; text-transform: uppercase; color: #c9a84c; margin-bottom: 1rem; }
  .score-bar-wrap { margin-bottom: 0.5rem; }
  .score-label { font-size: 0.6rem; letter-spacing: 0.18em; text-transform: uppercase; color: #8a7a50; margin-bottom: 0.2rem; }
  .score-bar-bg { background: rgba(201,168,76,0.15); height: 5px; width: 100%; }
  .score-bar-fill { height: 5px; background: linear-gradient(90deg, #6b4e1a, #c9a84c, #f5e080); }
  .score-num { font-family: 'Cormorant Garamond', serif; font-size: 1rem; color: #c9a84c; float: right; margin-top: -1.1rem; }
  .tech-bar-fill { height: 5px; background: linear-gradient(90deg, #4a7a6a, #6ab89a, #a0d4b8); }
  .section-divider { font-size: 0.55rem; letter-spacing: 0.4em; text-transform: uppercase; color: #c9a84c; margin: 1rem 0 0.6rem; padding-bottom: 0.3rem; border-bottom: 1px solid rgba(201,168,76,0.2); }
  .pass-badge { display: inline-block; padding: 0.2rem 0.8rem; font-size: 0.58rem; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 500; margin-left: 0.5rem; }
  .badge-pass { background: rgba(76,201,120,0.15); color: #2a8a50; border: 1px solid #2a8a50; }
  .badge-fail { background: rgba(201,76,76,0.15); color: #c94c4c; border: 1px solid #c94c4c; }
  .badge-warn { background: rgba(201,168,76,0.15); color: #8a6a10; border: 1px solid #c9a84c; }
  .badge-na   { background: rgba(100,100,100,0.1); color: #888; border: 1px solid #ccc; }
  .person-badge-yes { display:inline-block; padding:0.15rem 0.6rem; font-size:0.58rem; letter-spacing:0.15em; text-transform:uppercase; background:rgba(76,201,120,0.15); color:#2a8a50; border:1px solid #2a8a50; }
  .person-badge-no  { display:inline-block; padding:0.15rem 0.6rem; font-size:0.58rem; letter-spacing:0.15em; text-transform:uppercase; background:rgba(201,76,76,0.15); color:#c94c4c; border:1px solid #c94c4c; }
  .colour-swatch { display:inline-block; width:18px; height:18px; border-radius:50%; margin-right:4px; border:1px solid rgba(0,0,0,0.1); vertical-align:middle; }
  .session-stat { background: rgba(201,168,76,0.08); border: 1px solid rgba(201,168,76,0.25); padding: 1rem 1.5rem; text-align: center; }
  .stat-num { font-family: 'Cormorant Garamond', serif; font-size: 2.5rem; color: #c9a84c; line-height: 1; }
  .stat-label { font-size: 0.58rem; letter-spacing: 0.25em; text-transform: uppercase; color: #8a7a50; margin-top: 0.3rem; }
  .prompt-box { background: #f5edd8; border-left: 2px solid #c9a84c; padding: 0.8rem 1rem; font-size: 0.78rem; color: #6b5a30; font-style: italic; line-height: 1.6; margin-top: 0.8rem; }
  .reasoning-box { font-size: 0.75rem; color: #8a7a50; font-style: italic; line-height: 1.6; margin-top: 0.6rem; padding-top: 0.6rem; border-top: 1px solid rgba(201,168,76,0.1); }
  .section-title { font-size: 0.6rem; letter-spacing: 0.4em; text-transform: uppercase; color: #c9a84c; margin-bottom: 1.2rem; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(201,168,76,0.3); }
  .error-box { background: rgba(201,76,76,0.08); border: 1px solid rgba(201,76,76,0.3); padding: 1rem; color: #c94c4c; font-size: 0.85rem; }
  .img-missing { background: #f5edd8; border: 1px dashed rgba(201,168,76,0.3); display: flex; align-items: center; justify-content: center; height: 300px; color: #8a7a50; font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase; }
  .wait-banner { background: #f5edd8; border: 1px solid rgba(201,168,76,0.4); border-left: 3px solid #c9a84c; padding: 1rem 1.5rem; margin-bottom: 1.5rem; font-size: 0.78rem; color: #6b5a30; line-height: 1.7; }
  .wait-banner strong { color: #1c1608; }
  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

components.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@200;300;400&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background: #faf6ee; }
.header { background: #faf6ee; border-bottom: 1px solid rgba(201,168,76,0.3); padding: 2rem 3rem 1.5rem; display: flex; justify-content: space-between; align-items: flex-end; }
.title-block .eyebrow { font-family: 'Jost', sans-serif; font-weight: 200; font-size: 0.58rem; letter-spacing: 0.45em; text-transform: uppercase; color: #c9a84c; margin-bottom: 0.5rem; }
.title-block h1 { font-family: 'Cormorant Garamond', serif; font-size: 2.8rem; font-weight: 300; color: #1c1608; line-height: 1; }
.title-block h1 em { font-style: italic; }
.title-block h1 span { background: linear-gradient(135deg, #6b4e1a, #c9a84c, #a07828, #c9a84c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.meta { font-family: 'Jost', sans-serif; font-weight: 200; font-size: 0.62rem; letter-spacing: 0.25em; text-transform: uppercase; color: #8a7a50; text-align: right; }
</style>
</head>
<body>
<div class="header">
  <div class="title-block">
    <div class="eyebrow">Image Generation QA Pipeline</div>
    <h1><em>Mi</em> <span>Armoire</span> — Eval</h1>
  </div>
  <div class="meta">FLUX.1-schnell · LangGraph · Groq<br>Groq Vision Scorer · OpenCV Technical</div>
</div>
</body>
</html>
""", height=120)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

hf_token = os.environ.get("HF_TOKEN", "")
groq_key = os.environ.get("GROQ_API_KEY", "")

with st.sidebar:
    st.markdown("<div class='section-title'>Test Selection</div>", unsafe_allow_html=True)
    test_options = {f"[{t['id']}] {t['label']}": t["id"] for t in TEST_PROMPTS}
    selected_labels = st.multiselect("Select tests to run", options=list(test_options.keys()), default=list(test_options.keys())[:1])
    selected_ids = [test_options[l] for l in selected_labels]
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Past Results</div>", unsafe_allow_html=True)
    results_dir = os.path.join(os.path.dirname(__file__), "eval_results")
    result_files = sorted(glob.glob(os.path.join(results_dir, "results_*.json")), reverse=True)
    result_labels = ["-- Run new eval --"] + [os.path.basename(f) for f in result_files]
    selected_result_file = st.selectbox("Load past results", result_labels)

if "eval_results" not in st.session_state:
    st.session_state.eval_results = None

if selected_result_file != "-- Run new eval --" and st.session_state.eval_results is None:
    with open(os.path.join(results_dir, selected_result_file), encoding="utf-8") as f:
        st.session_state.eval_results = json.load(f)

col_run, col_clear = st.columns([2, 1])
with col_run:
    run_clicked = st.button("Run Eval Pipeline", use_container_width=True)
with col_clear:
    if st.button("Clear Results", use_container_width=True):
        st.session_state.eval_results = None
        st.rerun()

if run_clicked:
    if not selected_ids:
        st.warning("Select at least one test.")
    else:
        if hf_token: os.environ["HF_TOKEN"] = hf_token
        if groq_key: os.environ["GROQ_API_KEY"] = groq_key
        st.markdown("<div class='wait-banner'><strong>This will take a few minutes.</strong><br>HuggingFace credits are depleted — images via Pollinations.ai (~45s each). Each look runs OpenCV technical analysis + Groq vision scoring. Credits reset <strong>1st May 2026</strong>.</div>", unsafe_allow_html=True)
        from run_eval import run_eval
        progress_text = st.empty()
        progress_bar = st.progress(0)
        results = []
        for i, tid in enumerate(selected_ids):
            progress_text.markdown(f"<div style='font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;color:#c9a84c'>Running {tid} ({i+1}/{len(selected_ids)})...</div>", unsafe_allow_html=True)
            r = run_eval(test_ids=[tid])
            results.extend(r)
            progress_bar.progress((i + 1) / len(selected_ids))
        progress_text.empty()
        progress_bar.empty()
        st.session_state.eval_results = results
        st.rerun()


def score_badge(avg):
    if avg is None: return "<span class='pass-badge badge-na'>N/A</span>"
    elif avg >= 4.0: return "<span class='pass-badge badge-pass'>Pass</span>"
    elif avg >= 3.0: return "<span class='pass-badge badge-warn'>Borderline</span>"
    else: return "<span class='pass-badge badge-fail'>Fail</span>"

def ai_score_bar(label, score):
    pct = (score / 5) * 100 if score else 0
    display = f"{score}/5" if score else "-"
    return f"<div class='score-bar-wrap'><div class='score-label'>{label}</div><div class='score-bar-bg'><div class='score-bar-fill' style='width:{pct}%'></div></div><div class='score-num'>{display}</div><div style='clear:both'></div></div>"

def tech_score_bar(label, value, max_val, unit=""):
    if value is None: pct, display = 0, "-"
    else: pct, display = min((value / max_val) * 100, 100), f"{value}{unit}"
    return f"<div class='score-bar-wrap'><div class='score-label'>{label}</div><div class='score-bar-bg'><div class='tech-bar-fill' style='width:{pct}%'></div></div><div class='score-num' style='color:#6ab89a'>{display}</div><div style='clear:both'></div></div>"

AI_SCORE_LABELS = {
    "prompt_adherence": "Prompt Adherence", "visual_quality": "Visual Quality",
    "fashion_coherence": "Fashion Coherence", "occasion_fit": "Occasion Fit",
    "body_awareness": "Body Awareness", "garment_count_accuracy": "Garment Count Accuracy",
    "background_cleanliness": "Background Cleanliness", "lighting_consistency": "Lighting Consistency",
    "skin_tone_consistency": "Skin Tone Consistency", "style_consistency": "Style Consistency",
}

if st.session_state.eval_results:
    results = st.session_state.eval_results
    all_avgs = [r["session_avg"] for r in results if r.get("session_avg")]
    total_looks = sum(len(r.get("looks", [])) for r in results)
    looks_ok = sum(1 for r in results for l in r.get("looks", []) if l.get("image_status") == "ok")

    st.markdown("<div class='section-title'>Session Summary</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        (f"{round(sum(all_avgs)/len(all_avgs), 1)}/5" if all_avgs else "-", "Overall Avg Score"),
        (f"{len(results)}", "Tests Run"),
        (f"{looks_ok}/{total_looks}", "Images Generated"),
        (f"{sum(1 for a in all_avgs if a >= 3.5)}/{len(all_avgs)}" if all_avgs else "-", "Tests Passed"),
    ]
    for col, (num, label) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(f"<div class='session-stat'><div class='stat-num'>{num}</div><div class='stat-label'>{label}</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    for test in results:
        avg = test.get("session_avg")
        st.markdown(f"<div class='section-title'>[{test['id']}] {test['label']} {score_badge(avg)}<span style='float:right;font-family:Cormorant Garamond,serif;font-size:1rem;color:#c9a84c'>Session avg {avg}/5</span></div>", unsafe_allow_html=True)
        if test.get("error"):
            st.markdown(f"<div class='error-box'>Error: {test['error']}</div>", unsafe_allow_html=True)
            continue

        for look in test.get("looks", []):
            with st.expander(f"Look {look['look_index']} - {look['outfit_name']}", expanded=True):
                img_col, score_col = st.columns([1, 1])
                with img_col:
                    img_path = look.get("image_path")
                    if img_path and os.path.exists(img_path):
                        st.image(img_path, use_container_width=True)
                    else:
                        st.markdown(f"<div class='img-missing'>Image {look.get('image_status', 'missing')}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='prompt-box'>{look.get('image_prompt', '')}</div>", unsafe_allow_html=True)

                    tech = look.get("technical", {})
                    if any(v is not None for v in tech.values()):
                        st.markdown("<div class='section-divider'>Technical Metrics</div>", unsafe_allow_html=True)
                        has_person = tech.get("has_person")
                        if has_person is not None:
                            badge = "<span class='person-badge-yes'>Person Detected</span>" if has_person else "<span class='person-badge-no'>No Person Detected</span>"
                            st.markdown(badge, unsafe_allow_html=True)
                            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='font-size:0.7rem;color:#8a7a50;margin-bottom:0.6rem'>Resolution: <strong style='color:#1c1608'>{tech.get('resolution', '-')}</strong> &nbsp;·&nbsp; Aspect Ratio: <strong style='color:#1c1608'>{tech.get('aspect_ratio', '-')}</strong></div>", unsafe_allow_html=True)
                        st.markdown(tech_score_bar("Sharpness", tech.get("sharpness"), 100), unsafe_allow_html=True)
                        st.markdown(tech_score_bar("Brightness", tech.get("brightness"), 255), unsafe_allow_html=True)
                        st.markdown(tech_score_bar("Contrast", tech.get("contrast"), 128), unsafe_allow_html=True)
                        colours = tech.get("dominant_colours", [])
                        if colours:
                            swatches = "".join([f"<span class='colour-swatch' style='background:{c}' title='{c}'></span>" for c in colours])
                            st.markdown(f"<div style='font-size:0.6rem;letter-spacing:0.15em;text-transform:uppercase;color:#8a7a50;margin-top:0.6rem;margin-bottom:0.3rem'>Dominant Colours</div><div>{swatches} <span style='font-size:0.72rem;color:#8a7a50'>{' '.join(colours)}</span></div>", unsafe_allow_html=True)

                with score_col:
                    st.markdown(f"<div class='look-header'>{look['outfit_name']}</div><div class='look-meta'>{look.get('occasion', '')} · Jewellery: {look.get('jewellery', 'none')}</div>", unsafe_allow_html=True)
                    st.markdown("**Items:** " + ", ".join(look.get("items", [])))
                    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
                    st.markdown("<div class='section-divider'>AI Evaluation Scores</div>", unsafe_allow_html=True)
                    for dim in ["prompt_adherence", "visual_quality", "fashion_coherence", "occasion_fit", "body_awareness"]:
                        st.markdown(ai_score_bar(AI_SCORE_LABELS[dim], look["scores"].get(dim)), unsafe_allow_html=True)
                    st.markdown("<div class='section-divider' style='margin-top:0.8rem'>Extended Quality Scores</div>", unsafe_allow_html=True)
                    for dim in ["garment_count_accuracy", "background_cleanliness", "lighting_consistency", "skin_tone_consistency", "style_consistency"]:
                        st.markdown(ai_score_bar(AI_SCORE_LABELS[dim], look["scores"].get(dim)), unsafe_allow_html=True)
                    look_avg = look.get("look_avg")
                    st.markdown(f"<div style='margin-top:0.8rem;font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:#8a7a50'>Look Avg: <strong style='color:#c9a84c'>{look_avg}/5</strong> {score_badge(look_avg)}</div>", unsafe_allow_html=True)
                    if look.get("reasoning"):
                        st.markdown(f"<div class='reasoning-box'>{look['reasoning']}</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

else:
    st.markdown("<div style='text-align:center;padding:5rem 0;'><div style='font-family:Cormorant Garamond,serif;font-size:3rem;color:rgba(201,168,76,0.5);margin-bottom:1rem'>Mi Armoire</div><div style='font-size:0.65rem;letter-spacing:0.4em;text-transform:uppercase;color:#8a7a50'>Select tests on the left and click Run Eval Pipeline</div></div>", unsafe_allow_html=True)