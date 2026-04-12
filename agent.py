import os
import json
import re
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

# ── State ──────────────────────────────────────────────────────────────────────
class WardrobeState(TypedDict):
    user_input: str
    wardrobe: Dict[str, Any]
    outfits: List[Dict[str, str]]
    image_prompts: List[str]
    images: List[str]          # base64 or URL strings
    error: str

# ── LLM ───────────────────────────────────────────────────────────────────────
llm = ChatOllama(model="gemma3:4b", temperature=0.7)

# ── Node 1: Parse wardrobe + body info ────────────────────────────────────────
def parse_wardrobe(state: WardrobeState) -> WardrobeState:
    """Extract clothing items, accessories, and body measurements from free text."""
    prompt = f"""
You are a wardrobe parser. Extract all clothing items, accessories, jewellery, shoes, and body measurements from the user's description.

Return ONLY valid JSON in this exact format (no markdown, no extra text):
{{
  "tops": ["item1", "item2"],
  "bottoms": ["item1", "item2"],
  "shoes": ["item1", "item2"],
  "accessories": ["item1"],
  "jewellery": ["item1"],
  "body": {{
    "height": "value",
    "weight": "value",
    "notes": "any body shape notes inferred"
  }}
}}

User description:
{state['user_input']}
"""
    response = llm.invoke(prompt)
    raw = response.content.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        wardrobe = json.loads(raw)
    except json.JSONDecodeError:
        # Graceful fallback
        wardrobe = {"raw": state["user_input"], "tops": [], "bottoms": [], "shoes": [], "accessories": [], "jewellery": [], "body": {}}

    return {**state, "wardrobe": wardrobe}


# ── Node 2: Generate outfit combos ─────────────────────────────────────────────
def generate_outfits(state: WardrobeState) -> WardrobeState:
    """Create 4-5 styled outfit combinations with body-type-aware advice."""
    wardrobe_str = json.dumps(state["wardrobe"], indent=2)
    prompt = f"""
You are a professional personal stylist. Based on the wardrobe and body measurements below, create 4 distinct outfit combinations.

Wardrobe:
{wardrobe_str}

Rules:
- Only use items from the wardrobe provided
- Factor in the person's height and weight for silhouette advice
- Each outfit should have a name, occasion, and styling tip
- Consider colour coordination and balance

Return ONLY valid JSON — no markdown, no explanation:
[
  {{
    "name": "Outfit name",
    "occasion": "Where to wear this",
    "items": ["item1", "item2", "item3"],
    "jewellery": "gold/silver suggestion or 'none'",
    "tip": "One short styling tip relevant to their body type"
  }}
]

Return exactly 4 outfits.
"""
    response = llm.invoke(prompt)
    raw = response.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        outfits = json.loads(raw)
    except json.JSONDecodeError:
        outfits = [{"name": "Casual Day", "occasion": "Everyday", "items": list(state["wardrobe"].get("tops", []))[:2], "jewellery": "gold", "tip": "Keep it simple and comfortable."}]

    return {**state, "outfits": outfits}


# ── Node 3: Build image generation prompts ─────────────────────────────────────
def build_image_prompts(state: WardrobeState) -> WardrobeState:
    """Convert each outfit combo into a detailed Stable Diffusion prompt."""
    body = state["wardrobe"].get("body", {})
    height = body.get("height", "average height")
    prompts = []

    for outfit in state["outfits"]:
        items_str = ", ".join(outfit.get("items", []))
        jewellery = outfit.get("jewellery", "none")
        occasion = outfit.get("occasion", "")

        jewellery_clause = f", wearing {jewellery} jewellery" if jewellery != "none" else ""
        prompt = (
            f"fashion editorial photography, full body shot, "
            f"woman wearing {items_str}{jewellery_clause}, "
            f"height {height}, "
            f"{occasion} setting, "
            f"soft natural lighting, clean minimal background, "
            f"high quality, sharp focus, professional fashion shoot, "
            f"8k, photorealistic"
        )
        prompts.append(prompt)

    return {**state, "image_prompts": prompts}


# ── Node 4: Generate images via HuggingFace ────────────────────────────────────
def generate_images(state: WardrobeState) -> WardrobeState:
    """Call HuggingFace Inference API to generate outfit images."""
    import requests
    import base64

    hf_token = os.environ.get("HF_TOKEN", "")
    if not hf_token:
        return {**state, "error": "HF_TOKEN not set", "images": [""] * len(state["image_prompts"])}

    headers = {"Authorization": f"Bearer {hf_token}"}
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

    images = []
    for prompt in state["image_prompts"]:
        try:
            response = requests.post(
                api_url,
                headers=headers,
                json={"inputs": prompt, "parameters": {"num_inference_steps": 25, "guidance_scale": 7.5}},
                timeout=120
            )
            if response.status_code == 200:
                b64 = base64.b64encode(response.content).decode("utf-8")
                images.append(f"data:image/jpeg;base64,{b64}")
            elif response.status_code == 503:
                # Model loading — return placeholder
                images.append("loading")
            else:
                images.append("error")
        except Exception as e:
            images.append("error")

    return {**state, "images": images}


# ── Build graph ────────────────────────────────────────────────────────────────
def build_graph():
    graph = StateGraph(WardrobeState)

    graph.add_node("parse_wardrobe", parse_wardrobe)
    graph.add_node("generate_outfits", generate_outfits)
    graph.add_node("build_image_prompts", build_image_prompts)
    graph.add_node("generate_images", generate_images)

    graph.set_entry_point("parse_wardrobe")
    graph.add_edge("parse_wardrobe", "generate_outfits")
    graph.add_edge("generate_outfits", "build_image_prompts")
    graph.add_edge("build_image_prompts", "generate_images")
    graph.add_edge("generate_images", END)

    return graph.compile()


styling_agent = build_graph()


def run_agent(user_input: str) -> WardrobeState:
    initial_state: WardrobeState = {
        "user_input": user_input,
        "wardrobe": {},
        "outfits": [],
        "image_prompts": [],
        "images": [],
        "error": ""
    }
    return styling_agent.invoke(initial_state)