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

