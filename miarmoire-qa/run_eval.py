"""
Mi Armoire — Automated Image Generation Eval Script
Runs test prompts → generates images → scores each with Groq vision API
Outputs: eval_results/results.json + eval_results/report.md

Usage:
    python run_eval.py

Requirements:
    pip install requests python-dotenv
    Set in .env: GROQ_API_KEY, HF_TOKEN
"""

import os
import sys
import json
import base64
import time
import re
import datetime
import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

from test_prompts import TEST_PROMPTS

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
HF_TOKEN = os.environ.get("HF_TOKEN", "")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "eval_results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

EVAL_DIMENSIONS = [
    "prompt_adherence",
    "visual_quality",
    "fashion_coherence",
    "occasion_fit",
    "body_awareness",
]

SCORE_LABELS = {
    "prompt_adherence": "Prompt Adherence",
    "visual_quality": "Visual Quality",
    "fashion_coherence": "Fashion Coherence",
    "occasion_fit": "Occasion Fit",
    "body_awareness": "Body Awareness",
}


def run_miarmoire(input_text: str, occasion: str) -> dict:
    from agent import run_agent
    print(f"    -> Running agent...")
    return run_agent(input_text, occasion)


def score_image(image_b64: str, prompt: str, outfit: dict, occasion: str) -> dict:
    if not GROQ_API_KEY:
        print("    ! No GROQ_API_KEY - skipping auto-score")
        return {d: None for d in EVAL_DIMENSIONS}

    if image_b64.startswith("data:"):
        image_b64 = image_b64.split(",", 1)[1]

    system_prompt = """You are an expert image generation QA evaluator for a fashion AI system.
Score the image on exactly these 5 dimensions, each from 1 to 5:

1. prompt_adherence - do the garments/colours/accessories match what was requested?
2. visual_quality - sharpness, realism, no artifacts or distorted anatomy
3. fashion_coherence - does the outfit make sense as a real styled look?
4. occasion_fit - does the image setting/mood match the stated occasion?
5. body_awareness - does the body type/height seem to reflect the described person?

Return ONLY valid JSON, no markdown, no explanation:
{
  "prompt_adherence": <int 1-5>,
  "visual_quality": <int 1-5>,
  "fashion_coherence": <int 1-5>,
  "occasion_fit": <int 1-5>,
  "body_awareness": <int 1-5>,
  "reasoning": "<one sentence per dimension, comma-separated>"
}"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "max_tokens": 512,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                f"Image prompt used: {prompt}\n\n"
                                f"Outfit name: {outfit.get('name', '')}\n"
                                f"Occasion: {occasion}\n"
                                f"Items: {', '.join(outfit.get('items', []))}\n"
                                f"Jewellery: {outfit.get('jewellery', 'none')}\n\n"
                                "Please score this image."
                            ),
                        },
                    ],
                },
            ],
        },
        timeout=60,
    )

    if response.status_code != 200:
        print(f"    ! Groq API error {response.status_code}: {response.text[:200]}")
        return {d: None for d in EVAL_DIMENSIONS}

    raw = response.json()["choices"][0]["message"]["content"].strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"    ! Could not parse score JSON: {raw[:100]}")
        return {d: None for d in EVAL_DIMENSIONS}


def save_image(b64_data: str, test_id: str, look_idx: int) -> str:
    if not b64_data or b64_data in ("loading", "error", ""):
        return None
    if b64_data.startswith("data:"):
        b64_data = b64_data.split(",", 1)[1]
    img_path = os.path.join(OUTPUT_DIR, f"{test_id}_look{look_idx + 1}.jpg")
    with open(img_path, "wb") as f:
        f.write(base64.b64decode(b64_data))
    return img_path


def run_eval(test_ids: list = None):
    prompts = TEST_PROMPTS
    if test_ids:
        prompts = [p for p in prompts if p["id"] in test_ids]

    all_results = []
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n{'='*60}")
    print(f"  MI ARMOIRE IMAGE GEN EVAL - {timestamp}")
    print(f"  Running {len(prompts)} test(s)")
    print(f"{'='*60}\n")

    for test in prompts:
        print(f"> [{test['id']}] {test['label']}")
        test_result = {
            "id": test["id"],
            "label": test["label"],
            "occasion": test["occasion"],
            "input": test["input"],
            "looks": [],
            "session_consistency": None,
            "session_avg": None,
        }

        try:
            state = run_miarmoire(test["input"], test["occasion"])
        except Exception as e:
            print(f"    x Agent failed: {e}")
            test_result["error"] = str(e)
            all_results.append(test_result)
            continue

        outfits = state.get("outfits", [])
        images = state.get("images", [])
        prompts_used = state.get("image_prompts", [])

        print(f"    -> Generated {len(outfits)} outfits, {len(images)} images")

        look_scores = []

        for i, (outfit, image, img_prompt) in enumerate(zip(outfits, images, prompts_used)):
            print(f"    -> Scoring Look {i + 1}: {outfit.get('name', '?')}")

            img_path = save_image(image, test["id"], i)
            is_valid_image = img_path is not None

            if is_valid_image:
                scores = score_image(image, img_prompt, outfit, test["occasion"])
            else:
                print(f"      ! Image missing or error - status: {image}")
                scores = {d: None for d in EVAL_DIMENSIONS}

            dim_scores = {k: scores.get(k) for k in EVAL_DIMENSIONS}
            reasoning = scores.get("reasoning", "")
            valid_scores = [v for v in dim_scores.values() if v is not None]
            look_avg = round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else None

            look_result = {
                "look_index": i + 1,
                "outfit_name": outfit.get("name", ""),
                "occasion": outfit.get("occasion", ""),
                "items": outfit.get("items", []),
                "jewellery": outfit.get("jewellery", ""),
                "image_prompt": img_prompt,
                "image_path": img_path,
                "image_status": "ok" if is_valid_image else image,
                "scores": dim_scores,
                "reasoning": reasoning,
                "look_avg": look_avg,
            }
            test_result["looks"].append(look_result)
            if look_avg:
                look_scores.append(look_avg)

            print(f"      Scores: {dim_scores} | Avg: {look_avg}")
            time.sleep(1)

        vq_scores = [
            l["scores"].get("visual_quality")
            for l in test_result["looks"]
            if l["scores"].get("visual_quality")
        ]
        if len(vq_scores) >= 2:
            vq_range = max(vq_scores) - min(vq_scores)
            consistency = 5 if vq_range == 0 else (4 if vq_range == 1 else (3 if vq_range == 2 else 2))
            test_result["session_consistency"] = consistency

        test_result["session_avg"] = round(sum(look_scores) / len(look_scores), 2) if look_scores else None
        all_results.append(test_result)

        print(f"  [OK] [{test['id']}] Session avg: {test_result['session_avg']}\n")

    json_path = os.path.join(OUTPUT_DIR, f"results_{timestamp}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n[OK] Results saved: {json_path}")

    report_path = generate_report(all_results, timestamp)
    print(f"[OK] Report saved: {report_path}")

    return all_results


def generate_report(results: list, timestamp: str) -> str:
    lines = [
        "# Mi Armoire - Image Gen Eval Report",
        f"**Generated:** {timestamp}  ",
        f"**Tests run:** {len(results)}",
        "",
        "---",
        "",
    ]

    for test in results:
        lines += [
            f"## [{test['id']}] {test['label']}",
            f"**Occasion:** {test['occasion']}  ",
            f"**Session Avg Score:** {test.get('session_avg', 'N/A')} / 5  ",
            f"**Session Consistency:** {test.get('session_consistency', 'N/A')} / 5",
            "",
        ]

        if test.get("error"):
            lines.append(f"Error: {test['error']}")
            lines.append("")
            continue

        for look in test.get("looks", []):
            status_icon = "[OK]" if look["image_status"] == "ok" else "[FAIL]"
            lines += [
                f"### Look {look['look_index']}: {look['outfit_name']} {status_icon}",
                f"**Occasion:** {look['occasion']}  ",
                f"**Items:** {', '.join(look['items'])}  ",
                f"**Jewellery:** {look['jewellery']}  ",
                f"**Avg Score:** {look['look_avg']}",
                "",
                "| Dimension | Score |",
                "|-----------|-------|",
            ]
            for dim, label in SCORE_LABELS.items():
                score = look["scores"].get(dim)
                score_str = f"{score}/5" if score else "-"
                lines.append(f"| {label} | {score_str} |")

            if look.get("reasoning"):
                lines += ["", f"*{look['reasoning']}*"]
            lines.append("")

        lines.append("---")
        lines.append("")

    all_avgs = [r["session_avg"] for r in results if r.get("session_avg")]
    if all_avgs:
        overall = round(sum(all_avgs) / len(all_avgs), 2)
        lines += [
            "## Overall Summary",
            f"**Overall pipeline avg:** {overall} / 5",
            f"**Pass rate** (>= 3.5 avg): {sum(1 for a in all_avgs if a >= 3.5)}/{len(all_avgs)} tests",
        ]

    report_path = os.path.join(OUTPUT_DIR, f"report_{timestamp}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return report_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Mi Armoire Image Gen Eval")
    parser.add_argument("--ids", nargs="*", help="Specific test IDs to run, e.g. T01 T03")
    args = parser.parse_args()
    run_eval(test_ids=args.ids)