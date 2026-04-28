import streamlit as st
import streamlit.components.v1 as components
import os
import sys
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))
from agent import run_agent

st.set_page_config(
    page_title="Mi Armoire",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap');
  html, body, [class*="css"] { font-family: 'Jost', sans-serif; }
  .stApp { background: #faf6ee; color: #1c1608; }
  .stTextArea textarea {
    background: #fffdf5 !important; border: 1px solid #d4b86a !important;
    border-radius: 0 !important; color: #1c1608 !important;
    font-family: 'Jost', sans-serif !important; font-size: 0.9rem !important;
    font-weight: 300 !important; padding: 1.2rem !important;
    resize: none !important; line-height: 1.8 !important;
  }
  .stTextArea textarea:focus { border-color: #c9a84c !important; }
  .stTextArea textarea::placeholder { color: #b8a878 !important; font-style: italic !important; }
  .stTextArea label { display: none !important; }
  .stSelectbox > div > div {
    background: #fffdf5 !important; border: 1px solid #d4b86a !important;
    border-radius: 0 !important; color: #1c1608 !important;
  }
  .stSelectbox label {
    font-size: 0.62rem !important; letter-spacing: 0.2em !important;
    text-transform: uppercase !important; color: #c9a84c !important;
    font-weight: 300 !important;
  }
  .stButton > button {
    background: #1c1608 !important; color: #c9a84c !important;
    border: 1px solid #c9a84c !important; border-radius: 0 !important;
    padding: 0.85rem 2rem !important; font-family: 'Jost', sans-serif !important;
    font-size: 0.68rem !important; font-weight: 400 !important;
    letter-spacing: 0.3em !important; text-transform: uppercase !important;
    width: 100% !important; transition: all 0.3s !important;
  }
  .stButton > button:hover { background: #c9a84c !important; color: #1c1608 !important; }
  .form-label {
    font-size: 0.62rem; letter-spacing: 0.35em; text-transform: uppercase;
    color: #c9a84c; font-weight: 200; margin-bottom: 0.8rem;
    border-bottom: 1px solid #e8d5a0; padding-bottom: 0.5rem;
  }
  .outfit-info {
    padding: 2rem 2rem; border-right: 1px solid #e8d5a0; background: #faf6ee;
  }
  .outfit-num { font-size: 0.6rem; letter-spacing: 0.35em; text-transform: uppercase; color: #c9a84c; font-weight: 200; margin-bottom: 0.4rem; }
  .outfit-name { font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 400; color: #1c1608; line-height: 1.1; margin-bottom: 0.2rem; }
  .outfit-occasion { font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; color: #c9a84c; font-weight: 300; margin-bottom: 1.2rem; }
  .outfit-items { list-style: none; padding: 0; margin: 0 0 1rem; border-top: 1px solid #f0e6c8; padding-top: 0.8rem; }
  .outfit-item { font-size: 0.88rem; font-weight: 300; color: #4a3820; padding: 0.25rem 0; border-bottom: 1px solid #f8f0e0; }
  .outfit-item::before { content: '— '; color: #c9a84c; }
  .outfit-tip { font-family: 'Cormorant Garamond', serif; font-size: 1rem; font-style: italic; color: #8a7a50; line-height: 1.6; padding-top: 0.8rem; border-top: 1px solid #f0e6c8; }
  .gold-tag { display: inline-block; padding: 0.2rem 0.8rem; font-size: 0.62rem; letter-spacing: 0.15em; text-transform: uppercase; background: linear-gradient(135deg, #c9a84c, #e8cc7a); color: #1c1608; font-weight: 500; margin-bottom: 0.8rem; }
  .silver-tag { display: inline-block; padding: 0.2rem 0.8rem; font-size: 0.62rem; letter-spacing: 0.15em; text-transform: uppercase; background: #e8e8e8; color: #555; margin-bottom: 0.8rem; }
  .gold-rule { border: none; border-top: 1px solid #e8d5a0; margin: 0; }
  .wardrobe-panel { background: #1c1608; padding: 2rem 3rem; display: grid; grid-template-columns: repeat(5, 1fr); gap: 2rem; }
  .wardrobe-col-title { font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #c9a84c; font-weight: 200; margin-bottom: 0.6rem; padding-bottom: 0.3rem; border-bottom: 1px solid rgba(201,168,76,0.2); }
  .wardrobe-item { font-size: 0.78rem; font-weight: 300; color: rgba(250,246,238,0.7); padding: 0.15rem 0; }
  .body-pill { background: rgba(201,168,76,0.15); border: 1px solid rgba(201,168,76,0.3); color: #c9a84c; padding: 0.25rem 0.7rem; font-size: 0.72rem; display: inline-block; margin-bottom: 0.3rem; }
  .stSpinner > div { border-top-color: #c9a84c !important; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  section.main > div { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── HERO ───────────────────────────────────────────────────────────────────────
components.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@200;300;400&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #faf6ee; overflow: hidden; }
  .hero {
    width: 100%; min-height: 480px; background: #faf6ee;
    padding: 3.5rem 5rem 2.5rem;
    position: relative; overflow: hidden;
    border-bottom: 1px solid #e8d5a0;
  }
  .hero svg {
    position: absolute; top: 0; left: 0;
    width: 100%; height: 100%; pointer-events: none;
  }
  .hero-nav {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 3rem; position: relative; z-index: 2;
  }
  .hero-nav-left {
    font-family: 'Jost', sans-serif; font-weight: 200;
    font-size: 0.65rem; letter-spacing: 0.35em;
    text-transform: uppercase; color: #c9a84c;
  }
  .hero-nav-right {
    font-family: 'Jost', sans-serif; font-weight: 200;
    font-size: 0.6rem; letter-spacing: 0.22em;
    text-transform: uppercase; color: #b8a070;
  }
  .eyebrow {
    font-family: 'Jost', sans-serif; font-weight: 200;
    font-size: 0.6rem; letter-spacing: 0.42em;
    text-transform: uppercase; color: #c9a84c;
    margin-bottom: 0.8rem; position: relative; z-index: 2;
  }
  h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(4.5rem, 11vw, 9.5rem);
    font-weight: 400; line-height: 0.92; margin: 0 0 1.2rem;
    position: relative; z-index: 2;
    background: linear-gradient(135deg, #6b4e1a 0%, #c9a84c 28%, #f5e080 52%, #c9a84c 74%, #6b4e1a 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: 0.03em;
  }
  h1 em { font-style: italic; font-weight: 300; }
  .tagline {
    font-family: 'Jost', sans-serif; font-weight: 200;
    font-size: 0.7rem; letter-spacing: 0.28em;
    text-transform: uppercase; color: #8a7a50;
    position: relative; z-index: 2;
  }
</style>
</head>
<body>
<div class="hero">
  <svg viewBox="0 0 1400 480" xmlns="http://www.w3.org/2000/svg">
    <circle cx="110" cy="75" r="19" fill="#c9a84c" opacity="0.88"/>
    <circle cx="1290" cy="110" r="27" fill="#e8cc7a" opacity="0.82"/>
    <circle cx="1350" cy="370" r="13" fill="#c9a84c" opacity="0.68"/>
    <circle cx="55"  cy="370" r="11" fill="#e8cc7a" opacity="0.58"/>
    <circle cx="700" cy="35"  r="15" fill="#c9a84c" opacity="0.72"/>
    <circle cx="1110" cy="55" r="9"  fill="#c9a84c" opacity="0.48"/>
    <circle cx="210" cy="420" r="10" fill="#e8cc7a" opacity="0.58"/>
    <circle cx="950" cy="420" r="7"  fill="#c9a84c" opacity="0.42"/>
    <g stroke="#c9a84c" stroke-width="0.9" fill="none" opacity="0.32" transform="translate(590,95)">
      <ellipse cx="100" cy="100" rx="102" ry="102"/>
      <ellipse cx="100" cy="100" rx="102" ry="41"/>
      <ellipse cx="100" cy="100" rx="41"  ry="102"/>
      <line x1="100" y1="-2"  x2="100" y2="202"/>
      <line x1="-2"  y1="100" x2="202" y2="100"/>
      <line x1="18"  y1="28"  x2="182" y2="172"/>
      <line x1="182" y1="28"  x2="18"  y2="172"/>
      <line x1="8"   y1="60"  x2="192" y2="140"/>
      <line x1="8"   y1="140" x2="192" y2="60"/>
    </g>
    <ellipse cx="1060" cy="95" rx="66" ry="23" stroke="#c9a84c" stroke-width="4.5" fill="none" opacity="0.88" transform="rotate(-20 1060 95)"/>
    <polygon points="155,348 192,286 229,348" fill="#c9a84c" opacity="0.82"/>
    <polygon points="1185,358 1215,306 1245,358" fill="#e8cc7a" opacity="0.70"/>
    <polygon points="1160,385 1178,358 1196,385 1178,412" fill="#c9a84c" opacity="0.52"/>
    <polygon points="1290,235 1312,208 1334,235 1312,262" stroke="#c9a84c" stroke-width="1.5" fill="none" opacity="0.58"/>
    <polygon points="75,178 97,152 119,178 97,204"  stroke="#c9a84c" stroke-width="1.5" fill="none" opacity="0.48"/>
    <polygon points="480,38  496,18  512,38  496,58"  stroke="#c9a84c" stroke-width="1"   fill="none" opacity="0.38"/>
    <polygon points="1310,158 1322,140 1334,158 1322,176" fill="#c9a84c" opacity="0.58"/>
  </svg>
  <div class="hero-nav">
    <span class="hero-nav-left">Mi Armoire</span>
    <span class="hero-nav-right">Personal Style Atelier &nbsp;·&nbsp; Est. 2026</span>
  </div>
  <div class="eyebrow">Haute Collection &nbsp;·&nbsp; SS 2026</div>
  <h1>Mi <em>Armoire</em></h1>
  <div class="tagline">Where Style Meets Intention</div>
</div>
</body>
</html>
""", height=500)

# ── FORM + INFO COLUMNS ────────────────────────────────────────────────────────
left, right = st.columns([1, 1])

with left:
    st.markdown("""
<div style="background:#1c1608;padding:3rem 3.5rem;min-height:420px;display:flex;flex-direction:column;justify-content:center;">
  <div style="font-family:'Jost',sans-serif;font-weight:200;font-size:0.6rem;letter-spacing:0.35em;text-transform:uppercase;color:rgba(201,168,76,0.5);margin-bottom:1.2rem;">How It Works</div>
  <div style="font-family:'Cormorant Garamond',serif;font-size:1.7rem;font-weight:300;color:#faf6ee;line-height:1.55;margin-bottom:2rem;">Describe what you own.<br><em style="color:#c9a84c;">Receive curated looks.</em><br>No uploads. No effort.</div>
  <div style="font-family:'Cormorant Garamond',serif;font-size:0.88rem;font-weight:300;color:rgba(250,246,238,0.3);font-style:italic;line-height:1.9;">&ldquo;Style is a way to say who you are without having to speak.&rdquo;</div>
</div>
""", unsafe_allow_html=True)

with right:
    st.markdown('<div style="background:#faf6ee;padding:3rem 3.5rem;">', unsafe_allow_html=True)
    st.markdown('<div class="form-label">Describe Your Wardrobe</div>', unsafe_allow_html=True)

    example = (
        "I have a buttoned white formal shirt, black jumper with V neck and full sleeves, "
        "creamy trousers, blue jeans, dark blue skinny jeans, white sneakers and yellow/beige heels. "
        "My height is 4'11\" and weight is 60kg. I also have gold necklaces and silver hoop earrings."
    )

    if "wardrobe_text" not in st.session_state:
        st.session_state.wardrobe_text = ""

    user_input = st.text_area(
        "wardrobe",
        value=st.session_state.wardrobe_text,
        height=180,
        placeholder="Tell me what you own — clothes, shoes, jewellery, your height and weight…",
        label_visibility="collapsed"
    )

    col_a, col_b = st.columns(2)
    with col_a:
        num_looks = st.selectbox("Number of Looks", [2, 3, 4, 5], index=2)
    with col_b:
        occasion_filter = st.selectbox("Occasion", [
            "Any", "Casual", "Work / Office", "Evening Out",
            "Date Night", "Weekend Brunch", "Formal Event", "Gym / Active"
        ])

    c1, c2 = st.columns(2)
    with c1:
        go = st.button("✦  Compose Looks")
    with c2:
        if st.button("Use Example"):
            st.session_state.wardrobe_text = example
            st.rerun()

    if "results" in st.session_state and st.session_state.results:
        st.markdown("---")
        r1, r2 = st.columns(2)
        with r1:
            if st.button("↺  Regenerate"):
                with st.spinner("Regenerating…"):
                    try:
                        result = run_agent(st.session_state.last_input, st.session_state.get("last_occasion", "Any"))
                        st.session_state.results = result
                    except Exception as e:
                        st.error(str(e))
                st.rerun()
        with r2:
            if st.button("✕  Clear All"):
                st.session_state.results = None
                st.session_state.wardrobe_text = ""
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ── RUN AGENT ─────────────────────────────────────────────────────────────────
if go and user_input.strip():
    with st.spinner("Curating your looks…"):
        try:
            result = run_agent(user_input, occasion_filter)
            st.session_state.results = result
            st.session_state.last_input = user_input
            st.session_state.last_occasion = occasion_filter
        except Exception as e:
            st.error(f"Agent error: {e}")
            st.session_state.results = None
    st.rerun()
elif go and not user_input.strip():
    st.warning("Please describe your wardrobe first.")

# ── RESULTS ───────────────────────────────────────────────────────────────────
if "results" in st.session_state and st.session_state.results:
    result = st.session_state.results
    outfits = result.get("outfits", [])
    images  = result.get("images", [])
    wardrobe = result.get("wardrobe", {})

    st.markdown(f"""
<div style="background:#1c1608;padding:2rem 3rem;display:flex;align-items:center;justify-content:space-between;border-top:3px solid #c9a84c;">
  <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:300;color:#faf6ee;letter-spacing:0.06em;">Your Curated <em style="color:#c9a84c;">Looks</em></div>
  <div style="font-size:0.62rem;letter-spacing:0.25em;text-transform:uppercase;color:#c9a84c;font-weight:200;">{len(outfits)} looks composed</div>
</div>
""", unsafe_allow_html=True)

    for i, outfit in enumerate(outfits):
        info_col, img_col = st.columns([1, 1])

        j_raw = outfit.get("jewellery", "none")
        j_tag = ""
        if "gold" in j_raw.lower():
            j_tag = '<span class="gold-tag">✦ Gold</span>'
        elif "silver" in j_raw.lower():
            j_tag = '<span class="silver-tag">✦ Silver</span>'

        items_html = "".join([f'<li class="outfit-item">{item}</li>' for item in outfit.get("items", [])])

        with info_col:
            st.markdown(f"""
<div class="outfit-info">
  <div class="outfit-num">Look {i+1:02d}</div>
  <div class="outfit-name">{outfit.get('name', f'Look {i+1}')}</div>
  <div class="outfit-occasion">{outfit.get('occasion', '')}</div>
  {j_tag}
  <ul class="outfit-items">{items_html}</ul>
  <div class="outfit-tip">&ldquo;{outfit.get('tip', '')}&rdquo;</div>
</div>
""", unsafe_allow_html=True)

        with img_col:
            if i < len(images) and images[i] and images[i] not in ("error", "loading", "auth_error", ""):
                st.image(images[i], use_container_width=True)
            else:
                st.markdown("""
<div style="background:#f5f0e8;min-height:380px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.2rem;padding:2rem;">
  <div style="width:28px;height:28px;border:1px solid #c9a84c;transform:rotate(45deg);"></div>
  <span style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:#c9a84c;letter-spacing:0.05em;">Image Generation Paused</span>
  <span style="font-family:'Cormorant Garamond',serif;font-size:0.92rem;font-style:italic;color:#8a7a50;text-align:center;line-height:1.8;max-width:300px;">
    Monthly HuggingFace credits have been reached.<br>
    Full image generation resumes <strong style="color:#c9a84c;">1st May 2026</strong>.
  </span>
</div>""", unsafe_allow_html=True)

        st.markdown('<hr class="gold-rule">', unsafe_allow_html=True)

    # Wardrobe breakdown
    body = wardrobe.get("body", {})
    tops = wardrobe.get("tops", [])
    bottoms = wardrobe.get("bottoms", [])
    shoes = wardrobe.get("shoes", [])
    jewellery = wardrobe.get("jewellery", [])

    def witem(items):
        return "".join([f'<div class="wardrobe-item">— {i}</div>' for i in items]) or '<div class="wardrobe-item" style="opacity:0.3">—</div>'

    body_html = ""
    if body.get("height"): body_html += f'<div class="body-pill">H: {body["height"]}</div><br>'
    if body.get("weight"): body_html += f'<div class="body-pill">W: {body["weight"]}</div>'

    st.markdown(f"""
<div class="wardrobe-panel">
  <div><div class="wardrobe-col-title">Measurements</div>{body_html}</div>
  <div><div class="wardrobe-col-title">Tops</div>{witem(tops)}</div>
  <div><div class="wardrobe-col-title">Bottoms</div>{witem(bottoms)}</div>
  <div><div class="wardrobe-col-title">Shoes</div>{witem(shoes)}</div>
  <div><div class="wardrobe-col-title">Jewellery</div>{witem(jewellery)}</div>
</div>
""", unsafe_allow_html=True)