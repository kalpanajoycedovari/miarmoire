\# 🪞 Mi Armoire — AI Personal Styling Agent



> \*"Style is a way to say who you are without having to speak."\*



\---



\## The Story Behind This



I've always loved fashion. Not just wearing clothes — but the \*art\* of it. The way a well-chosen outfit can shift your entire energy before you walk out the door. The way accessories — a gold necklace, a pair of silver hoops — can take something simple and make it feel intentional. I find joy in the details: the way cream trousers pair with a crisp white shirt, the way heels change your silhouette, the way layering jewellery tells a story without saying a word.



But here's the thing — even I, someone who genuinely loves this, have stood in front of a full wardrobe and felt completely paralysed.



I know that feeling all too well. It's 8am. You have somewhere to be. You open your wardrobe and suddenly nothing makes sense. You have \*loads\* of clothes — you know you do — but nothing feels right, nothing goes together, and the clock is ticking. You start pulling things out, second-guessing yourself, and eventually just grab the same safe outfit you always wear when you can't think straight.



I've been there. And so have so many people I know.



It's not just about having clothes. It's about knowing how to \*use\* them. How to combine them. How to dress for your body, your occasion, your mood. That knowledge doesn't come automatically — and for a lot of people, it's genuinely stressful. Especially when you're trying to fit in, make a first impression, or just feel confident in your own skin.



That frustration is exactly what made me build \*\*Mi Armoire\*\*.



\---



\## What It Does



Mi Armoire is an AI personal styling agent that takes the panic out of getting dressed.



No photo uploads. No complicated interfaces. You just describe what you own — in plain text, however you naturally speak — and it generates curated outfit combinations tailored to your body measurements, the occasion you're dressing for, and the clothes you actually have.



It's for the person who has a wardrobe full of options but no idea what to do with them. It's for the person who wants to look put together but doesn't know where to start. It's for anyone who's ever stood in front of their clothes and thought \*I have nothing to wear\* — when really, they just needed a little help seeing the possibilities.

Mi Armoire — Agentic AI Styling System
Show Image
Show Image
Show Image
Show Image
Show Image
A production-deployed, multi-agent AI system that generates personalised outfit recommendations from a user's wardrobe inventory. Built on a modular LangGraph agent architecture with a live Streamlit interface.
Live: miarmoire.streamlit.app

What it does
Mi Armoire takes a user's uploaded wardrobe items and generates complete outfit recommendations with AI-produced style images. The system coordinates multiple specialised agents — one for wardrobe analysis, one for outfit composition, one for prompt construction, and one for image generation — each with a defined role and a single responsibility.
The result is an end-to-end agentic pipeline: structured input → multi-step reasoning → visual output, all running in a deployed application.

Architecture
User Input (wardrobe items + occasion)
        │
        ▼
┌─────────────────────────────────────────────┐
│              LangGraph Orchestrator          │
│  (stateful graph, node-based agent routing) │
└──────┬──────────────────────────────────────┘
       │
       ├──▶ Wardrobe Analyser Agent
       │     └─ Parses and categorises uploaded items
       │
       ├──▶ Outfit Composer Agent  
       │     └─ Selects combinations based on occasion + style rules
       │
       ├──▶ Prompt Engineer Agent
       │     └─ Constructs structured image generation prompts
       │
       └──▶ Image Generation Agent
             └─ Calls FLUX.1-schnell API → returns styled outfit image
LLM backbone: Groq-hosted llama-3.3-70b — chosen for low-latency inference suitable for real-time user-facing applications.
Image generation: FLUX.1-schnell via Hugging Face Inference API.
Frontend: Streamlit — stateful session management, file upload handling, and image rendering.

Tech stack
ComponentTechnologyAgent orchestrationLangGraph (stateful graph, conditional edges)LLM inferenceGroq API — llama-3.3-70bImage generationFLUX.1-schnell (Hugging Face Inference API)Application layerStreamlitLanguagePython 3.11DeploymentStreamlit Cloud (live, public)

Key engineering decisions
Why LangGraph over a single LLM call?
A monolithic prompt asking one model to analyse a wardrobe, compose an outfit, and write an image generation prompt produces inconsistent results. Decomposing this into a directed graph of specialised agents gives each node a narrow, verifiable task. It also makes the pipeline extensible — new agents (e.g. a weather-aware agent, a trend-lookup agent) can be added as nodes without rewriting existing logic.
Why Groq?
Outfit recommendation is a latency-sensitive, user-facing task. Groq's LPU inference delivers sub-second response times for 70B parameter models, which makes the experience feel responsive rather than batch-processed.
Why Streamlit for deployment?
The goal was a live, publicly accessible demo — not a local notebook. Streamlit Cloud handles deployment, secrets management, and session state out of the box, making it the right choice for a solo-deployed production application.

Agent design
Each agent in the graph is implemented as a Python function that takes the shared graph state and returns an updated state. Agents do not call each other directly — the LangGraph orchestrator manages routing via conditional edges.
python# Simplified node signature pattern used throughout
def outfit_composer_agent(state: GraphState) -> GraphState:
    wardrobe = state["analysed_wardrobe"]
    occasion = state["occasion"]
    # ... compose outfit from wardrobe items
    return {**state, "outfit": composed_outfit}
State is typed using a TypedDict schema, which enforces what each agent can read and write — a lightweight form of contract between agents.

Running locally
bashgit clone https://github.com/kalpanajoycedovari/miarmoire.git
cd miarmoire
pip install -r requirements.txt
Set environment variables:
GROQ_API_KEY=your_groq_key
HF_TOKEN=your_huggingface_token
bashstreamlit run app.py

Project structure
miarmoire/
├── app.py                  # Streamlit entry point, session state management
├── graph/
│   ├── state.py            # TypedDict state schema shared across agents
│   ├── nodes.py            # Individual agent functions (one per node)
│   └── pipeline.py         # LangGraph graph definition and edge routing
├── utils/
│   ├── image_gen.py        # FLUX.1-schnell API wrapper
│   └── prompt_builder.py   # Prompt construction utilities
└── requirements.txt

Relevance to AI/ML platform engineering
This project demonstrates several capabilities directly applicable to production AI/ML platform work:

Multi-agent system design — decomposing a complex task into a directed graph of specialised agents with defined interfaces
LLM integration in production — real API calls to inference providers with error handling, not local notebooks
Stateful pipeline orchestration — LangGraph manages state transitions between agents, analogous to how MLOps pipelines manage state between model training, evaluation, and deployment steps
Deployed application — live on Streamlit Cloud; not a demo that exists only on a local machine
Extensible architecture — adding a new capability (e.g. retrieval, tool use, a new agent) requires adding a node and an edge, not rewriting the pipeline





\---



\## Features



\- \*\*Text-only wardrobe input\*\* — describe your clothes in plain English, no uploads needed

\- \*\*Body-aware styling\*\* — factors in your height and weight for silhouette and proportion advice

\- \*\*Occasion filter\*\* — style for Casual, Work, Date Night, Evening Out, Formal, and more

\- \*\*Jewellery pairing\*\* — gold and silver suggestions per look

\- \*\*AI-generated outfit visuals\*\* — see your actual clothes styled together via FLUX image generation

\- \*\*Multiple looks\*\* — generate 2 to 5 outfit options at once

\- \*\*Regenerate\*\* — not feeling a look? Get a fresh set instantly



\---



\## Tech Stack



| Layer | Tool |

|-------|------|

| Agent framework | LangGraph |

| LLM | Groq — llama-3.3-70b-versatile |

| Image generation | FLUX.1-schnell via HuggingFace Inference API |

| UI | Streamlit |

| Deployment | Streamlit Cloud |



\---



\## Running Locally



\*\*Prerequisites:\*\*

\- Python 3.11+

\- A free \[HuggingFace](https://huggingface.co) account + token

\- A free \[Groq](https://console.groq.com) account + API key



```bash

git clone https://github.com/kalpanajoycedovari/miarmoire.git

cd miarmoire

python -m venv venv

venv\\Scripts\\activate  # Windows

pip install -r requirements.txt

```



Create a `.env` file:

```

HF\_TOKEN=hf\_yourtoken

GROQ\_API\_KEY=gsk\_yourkey

```



Run:

```bash

streamlit run app.py

```



\---



\## Live Demo



🌐 \*\*\[miarmoire.streamlit.app](https://miarmoire.streamlit.app)\*\*



\---



\## Example Input



```

I have a buttoned white formal shirt, black jumper with V neck and full sleeves,

creamy trousers, blue jeans, dark blue skinny jeans, white sneakers and yellow/beige heels.

My height is 4'11" and weight is 60kg. I also have gold necklaces and silver hoop earrings.

```



\---



\## About



Built by \*\*Kalpana Joyce Dovari\*\* — MSc Artificial Intelligence student at Northumbria University London, and someone who believes that knowing how to dress well shouldn't be a privilege or a mystery. Everyone deserves to open their wardrobe and feel confident about what they put on.



\*Mi Armoire\* means \*My Wardrobe\* in French — and that's exactly what this is. Yours. Understood. Styled.



\---



\*Built with love, a lot of outfit indecision, and way too much time spent staring at a wardrobe. 🪞✦\*

