import os
import json
import re
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

class WardrobeState(TypedDict):
    user_input: str
    wardrobe: Dict[str, Any]
    outfits: List[Dict[str, str]]
    image_prompts: List[str]
    images: List[str]
    error: str

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, api_key=os.environ.get("GROQ_API_KEY"))

def parse_wardrobe(state: WardrobeState) -> WardrobeState:
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
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        wardrobe = json.loads(raw)
    except json.JSONDecodeError:
        wardrobe = {"raw": state["user_input"], "tops": [], "bottoms": [], "shoes": [], "accessories": [], "jewellery": [], "body": {}}

    return {**state, "wardrobe": wardrobe}


def generate_outfits(state: WardrobeState) -> WardrobeState:
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

Return ONLY valid JSON - no markdown, no explanation:
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


def build_image_prompts(state: WardrobeState) -> WardrobeState:
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


def generate_images(state: WardrobeState) -> WardrobeState:
    """Call HuggingFace first, fall back to Pollinations.ai if credits depleted."""
    import requests
    import base64
    from urllib.parse import quote

    hf_token = os.environ.get("HF_TOKEN", "")
    headers = {"Authorization": f"Bearer {hf_token}"}
    hf_url = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

    images = []
    for prompt in state["image_prompts"]:
        image_data = None

        # Try HuggingFace first
        if hf_token:
            try:
                response = requests.post(
                    hf_url,
                    headers=headers,
                    json={"inputs": prompt},
                    timeout=120
                )
                if response.status_code == 200:
                    b64 = base64.b64encode(response.content).decode("utf-8")
                    image_data = f"data:image/jpeg;base64,{b64}"
                elif response.status_code in (402, 503):
                    print(f"    HF unavailable ({response.status_code}), falling back to Pollinations...")
                else:
                    print(f"    HF error {response.status_code}, falling back to Pollinations...")
            except Exception as e:
                print(f"    HF exception: {e}, falling back to Pollinations...")

        # Fall back to Pollinations.ai
        if not image_data:
            try:
                encoded_prompt = quote(prompt)
                poll_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=1024&nologo=true"
                response = requests.get(poll_url, timeout=120)
                if response.status_code == 200:
                    b64 = base64.b64encode(response.content).decode("utf-8")
                    image_data = f"data:image/jpeg;base64,{b64}"
                else:
                    print(f"    Pollinations error {response.status_code}")
                    image_data = "error"
            except Exception as e:
                print(f"    Pollinations exception: {e}")
                image_data = "error"

        images.append(image_data)

    return {**state, "images": images}


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


def run_agent(user_input: str, occasion: str = "Any") -> WardrobeState:
    occasion_clause = f" All outfits must be suitable for: {occasion}." if occasion != "Any" else ""
    initial_state: WardrobeState = {
        "user_input": user_input + occasion_clause,
        "wardrobe": {},
        "outfits": [],
        "image_prompts": [],
        "images": [],
        "error": ""
    }
    return styling_agent.invoke(initial_state)