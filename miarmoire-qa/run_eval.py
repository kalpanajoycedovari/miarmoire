"""
Mi Armoire — Automated Image Generation Eval Script
Technical + AI scoring pipeline
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

AI_DIMENSIONS = [
    "prompt_adherence",
    "visual_quality",
    "fashion_coherence",
    "occasion_fit",
    "body_awareness",
    "garment_count_accuracy",
    "background_cleanliness",
    "lighting_consistency",
    "skin_tone_consistency",
    "style_consistency",
]

SCORE_LABELS = {
    "prompt_adherence": "Prompt Adherence",
    "visual_quality": "Visual Quality",
    "fashion_coherence": "Fashion Coherence",
    "occasion_fit": "Occasion Fit",
    "body_awareness": "Body Awareness",
    "garment_count_accuracy": "Garment Count Accuracy",
    "background_cleanliness": "Background Cleanliness",
    "lighting_consistency": "Lighting Consistency",
    "skin_tone_consistency": "Skin Tone Consistency",
    "style_consistency": "Style Consistency",
}

TECH_LABELS = {
    "sharpness": "Sharpness (Blur Detection)",
    "brightness": "Brightness Level",
    "contrast": "Contrast Level",
    "has_person": "Person Detected",
    "resolution": "Resolution",
    "aspect_ratio": "Aspect Ratio",
    "dominant_colours": "Dominant Colours",
}


def compute_technical_metrics(img_path: str) -> dict:
    try:
        import cv2
        import numpy as np
        from PIL import Image

        img_pil = Image.open(img_path).convert("RGB")
        width, height = img_pil.size
        img_np = np.array(img_pil)
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        laplacian_var = cv2.Laplacian(img_gray, cv2.CV_64F).var()
        sharpness_score = min(round(laplacian_var / 100, 1), 100.0)
        brightness = round(float(np.mean(img_gray)), 1)
        contrast = round(float(np.std(img_gray)), 1)

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        img_resized = cv2.resize(img_np, (640, 480))
        img_bgr = cv2.cvtColor(img_resized, cv2.COLOR_RGB2BGR)
        rects, _ = hog.detectMultiScale(img_bgr, winStride=(8, 8), padding=(4, 4), scale=1.05)
        has_person = len(rects) > 0

        pixels = img_np.reshape(-1, 3).astype(np.float32)
        if len(pixels) > 5000:
            idx = np.random.choice(len(pixels), 5000, replace=False)
            pixels = pixels[idx]
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(pixels, 5, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        counts = np.bincount(labels.flatten())
        sorted_centers = centers[np.argsort(-counts)]
        dominant_colours = [
            "#{:02x}{:02x}{:02x}".format(int(c[0]), int(c[1]), int(c[2]))
            for c in sorted_centers[:5]
        ]

        return {
            "sharpness": sharpness_score,
            "brightness": brightness,
            "contrast": contrast,
            "has_person": has_person,
            "resolution": f"{width}x{height}",
            "aspect_ratio": round(width / height, 2),
            "dominant_colours": dominant_colours,
        }

    except Exception as e:
        print(f"      ! Technical metrics failed: {e}")
        return {
            "sharpness": None, "brightness": None, "contrast": None,
            "has_person": None, "resolution": None, "aspect_ratio": None,
            "dominant_colours": [],
        }


def score_image(image_b64: str, prompt: str, outfit: dict, occasion: str, all_outfits: list) -> dict:
    if not GROQ_API_KEY:
        print("    ! No GROQ_API_KEY - skipping auto-score")
        return {d: None for d in AI_DIMENSIONS}

    if image_b64.startswith("data:"):
        image_b64 = image_b64.split(",", 1)[1]

    items_count = len(outfit.get("items", []))
    all_occasions = ", ".join([o.get("occasion", "") for o in all_outfits])

    system_prompt = f"""You are an expert image generation QA evaluator for a fashion AI system.
Score the image on exactly these 10 dimensions, each from 1 to 5:

1. prompt_adherence - do the garments/colours/accessories match what was requested?
2. visual_quality - sharpness, realism, no artifacts or distorted anatomy
3. fashion_coherence - does the outfit make sense as a real styled look?
4. occasion_fit - does the image setting/mood match the stated occasion?
5. body_awareness - does the body type/height reflect the described person?
6. garment_count_accuracy - did all {items_count} requested items appear in the image?
7. background_cleanliness - is the background clean, minimal, and non-distracting?
8. lighting_consistency - is the lighting natural, even, and professional?
9. skin_tone_consistency - is the skin tone realistic and consistent throughout?
10. style_consistency - does this look consistent in style with the other occasions: {all_occasions}?

Return ONLY valid JSON, no markdown, no explanation:
{{
  "prompt_adherence": ,
  "visual_quality": ,
  "fashion_coherence": ,
  "occasion_fit": ,
  "body_awareness": ,
  "garment_count_accuracy": ,
  "background_cleanliness": ,
  "lighting_consistency": ,
  "skin_tone_consistency": ,
  "style_consistency": ,
  "reasoning": ""
}}"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "max_tokens": 700,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                    {"type": "text", "text": (
                        f"Image prompt: {prompt}\n"
                        f"Outfit: {outfit.get('name', '')}\n"
                        f"Occasion: {occasion}\n"
                        f"Items ({items_count}): {', '.join(outfit.get('items', []))}\n"
                        f"Jewellery: {outfit.get('jewellery', 'none')}\n"
                        "Please score this image on all 10 dimensions."
                    )},
                ]},
            ],
        },
        timeout=60,
    )

    if response.status_code != 200:
        print(f"    ! Groq error {response.status_code}: {response.text[:200]}")
        return {d: None for d in AI_DIMENSIONS}

    raw = response.json()["choices"][0]["message"]["content"].strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"    ! Could not parse score JSON: {raw[:100]}")
        return {d: None for d in AI_DIMENSIONS}


def save_image(b64_data: str, test_id: str, look_idx: int) -> str:
    if not b64_data or b64_data in ("loading", "error", ""):
        return None
    if b64_data.startswith("data:"):
        b64_data = b64_data.split(",", 1)[1]
    img_path = os.path.join(OUTPUT_DIR, f"{test_id}_look{look_idx + 1}.jpg")
    with open(img_path, "wb") as f:
        f.write(base64.b64decode(b64_data))
    return img_path


def run_miarmoire(input_text: str, occasion: str) -> dict:
    from agent import run_agent
    print(f"    -> Running agent...")
    return run_agent(input_text, occasion)


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
            "id": test["id"], "label": test["label"],
            "occasion": test["occasion"], "input": test["input"],
            "looks": [], "session_consistency": None, "session_avg": None,
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
        print(f"    -> {len(outfits)} outfits, {len(images)} images")

        look_scores = []

        for i, (outfit, image, img_prompt) in enumerate(zip(outfits, images, prompts_used)):
            print(f"    -> Scoring Look {i + 1}: {outfit.get('name', '?')}")

            img_path = save_image(image, test["id"], i)
            is_valid = img_path is not None

            tech = compute_technical_metrics(img_path) if is_valid else {k: None for k in TECH_LABELS}

            if is_valid:
                ai_scores = score_image(image, img_prompt, outfit, test["occasion"], outfits)
            else:
                print(f"      ! Image missing - status: {image}")
                ai_scores = {d: None for d in AI_DIMENSIONS}

            dim_scores = {k: ai_scores.get(k) for k in AI_DIMENSIONS}
            reasoning = ai_scores.get("reasoning", "")
            valid = [v for v in dim_scores.values() if v is not None]
            look_avg = round(sum(valid) / len(valid), 2) if valid else None

            look_result = {
                "look_index": i + 1,
                "outfit_name": outfit.get("name", ""),
                "occasion": outfit.get("occasion", ""),
                "items": outfit.get("items", []),
                "jewellery": outfit.get("jewellery", ""),
                "image_prompt": img_prompt,
                "image_path": img_path,
                "image_status": "ok" if is_valid else image,
                "scores": dim_scores,
                "technical": tech,
                "reasoning": reasoning,
                "look_avg": look_avg,
            }
            test_result["looks"].append(look_result)
            if look_avg:
                look_scores.append(look_avg)

            print(f"      AI: {dim_scores}")
            print(f"      Tech: sharpness={tech.get('sharpness')}, brightness={tech.get('brightness')}, person={tech.get('has_person')}")
            time.sleep(1)

        vq_scores = [l["scores"].get("visual_quality") for l in test_result["looks"] if l["scores"].get("visual_quality")]
        if len(vq_scores) >= 2:
            vq_range = max(vq_scores) - min(vq_scores)
            test_result["session_consistency"] = 5 if vq_range == 0 else (4 if vq_range == 1 else (3 if vq_range == 2 else 2))

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
        f"**Generated:** {timestamp}", f"**Tests run:** {len(results)}", "", "---", "",
    ]

    for test in results:
        lines += [
            f"## [{test['id']}] {test['label']}",
            f"**Occasion:** {test['occasion']}",
            f"**Session Avg:** {test.get('session_avg', 'N/A')} / 5",
            f"**Consistency:** {test.get('session_consistency', 'N/A')} / 5", "",
        ]

        if test.get("error"):
            lines.append(f"Error: {test['error']}")
            lines.append("")
            continue

        for look in test.get("looks", []):
            status = "[OK]" if look["image_status"] == "ok" else "[FAIL]"
            lines += [
                f"### Look {look['look_index']}: {look['outfit_name']} {status}",
                f"**Avg Score:** {look['look_avg']}", "",
                "#### AI Scores", "| Dimension | Score |", "|-----------|-------|",
            ]
            for dim, label in SCORE_LABELS.items():
                score = look["scores"].get(dim)
                lines.append(f"| {label} | {f'{score}/5' if score else '-'} |")

            tech = look.get("technical", {})
            lines += [
                "", "#### Technical Metrics", "| Metric | Value |", "|--------|-------|",
                f"| Sharpness | {tech.get('sharpness', '-')} |",
                f"| Brightness | {tech.get('brightness', '-')} |",
                f"| Contrast | {tech.get('contrast', '-')} |",
                f"| Person Detected | {tech.get('has_person', '-')} |",
                f"| Resolution | {tech.get('resolution', '-')} |",
                f"| Aspect Ratio | {tech.get('aspect_ratio', '-')} |",
                f"| Dominant Colours | {', '.join(tech.get('dominant_colours', []))} |",
            ]
            if look.get("reasoning"):
                lines += ["", f"*{look['reasoning']}*"]
            lines.append("")

        lines += ["---", ""]

    all_avgs = [r["session_avg"] for r in results if r.get("session_avg")]
    if all_avgs:
        overall = round(sum(all_avgs) / len(all_avgs), 2)
        lines += [
            "## Overall Summary",
            f"**Overall avg:** {overall} / 5",
            f"**Pass rate (>=3.5):** {sum(1 for a in all_avgs if a >= 3.5)}/{len(all_avgs)}",
        ]

    report_path = os.path.join(OUTPUT_DIR, f"report_{timestamp}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return report_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="*")
    args = parser.parse_args()
    run_eval(test_ids=args.ids)