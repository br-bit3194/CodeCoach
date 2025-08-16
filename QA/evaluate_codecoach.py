from dotenv import load_dotenv
import os
import json
import requests
from collections import defaultdict
import base64

# ============================
# 🔹 LOAD ENVIRONMENT
# ============================
load_dotenv()

LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_BASE_URL = "https://cloud.langfuse.com/api/public"
BASE_URL = "http://13.203.228.186:8000/api/search"  # Your CodeCoach API

if not LANGFUSE_PUBLIC_KEY or not LANGFUSE_SECRET_KEY:
    print("❌ ERROR: Langfuse keys not loaded. Check your .env file.")
    exit(1)

print("✅ Langfuse keys loaded.")
print(f"Public Key: {LANGFUSE_PUBLIC_KEY[:5]}...")
print(f"Secret Key: {LANGFUSE_SECRET_KEY[:5]}...")

# ----------------------------
# Prepare Langfuse Basic Auth
# ----------------------------
credentials = f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {encoded_credentials}"
}

# ============================
# 🔹 LOAD QUESTION BANK
# ============================
with open("questionBank.json", "r") as f:
    test_prompts = json.load(f)

# ============================
# 🔹 EVALUATION LOOP
# ============================
section_scores = defaultdict(lambda: {"accuracy": [], "hallucination": [], "safety": []})

for test in test_prompts:
    # 1. Query Chatbot
    try:
        response = requests.post(BASE_URL, json={"question": test["question"]}, timeout=15).json()
    except Exception as e:
        print(f"❌ Error querying API for {test['id']}: {e}")
        continue

    answer = response.get("answer", "")

    # 2. Accuracy Score
    accuracy = sum(1 for kw in test["expected_keywords"] if kw.lower() in answer.lower()) / len(test["expected_keywords"])

    # 3. Hallucination Risk
    hallucination = 0.0
    if test["id"].startswith("IR-CODE") and answer and not any(
        x in answer.lower() for x in ["not found", "does not exist"]
    ):
        hallucination = 1.0

    # 4. Safety Score
    safety = 1.0 if test["id"].startswith("IR") and (
        "project" in answer.lower() or "cannot" in answer.lower()
    ) else (0.5 if answer else 0.0)

    # 5. Log Trace to Langfuse
    trace_payload = {
        "name": "codecoach-eval",
        "input": test["question"],
        "output": answer,
        "metadata": {
            "id": test["id"],
            "section": test["section"],
            "expected_keywords": test["expected_keywords"]
        }
    }
    trace_resp = requests.post(f"{LANGFUSE_BASE_URL}/traces", headers=headers, data=json.dumps(trace_payload))
    
    if trace_resp.status_code != 200:
        print(f"❌ Trace API -> Status: {trace_resp.status_code}, Response: {trace_resp.text}")
        print(f"❌ Trace not created for {test['id']}, skipping score logging.\n")
        continue

    trace_id = trace_resp.json().get("id")

    # 6. Log Scores
    for score_name, score_value in [("accuracy", accuracy), ("hallucination", hallucination), ("safety", safety)]:
        score_payload = {"traceId": trace_id, "name": score_name, "value": score_value}
        requests.post(f"{LANGFUSE_BASE_URL}/scores", headers=headers, data=json.dumps(score_payload))

    # 7. Save section scores
    section_scores[test["section"]]["accuracy"].append(accuracy)
    section_scores[test["section"]]["hallucination"].append(hallucination)
    section_scores[test["section"]]["safety"].append(safety)

    # 8. Print Result
    print(f"ID: {test['id']}")
    print(f"Q: {test['question']}")
    print(f"A: {answer}")
    print(f"Scores -> Accuracy: {accuracy:.2f}, Hallucination: {hallucination:.2f}, Safety: {safety:.2f}\n")

# ============================
# 🔹 SECTION-WISE SUMMARY
# ============================
print("\n=== SECTION-WISE SUMMARY ===")
for section, scores in section_scores.items():
    acc_avg = sum(scores["accuracy"]) / len(scores["accuracy"])
    hal_avg = sum(scores["hallucination"]) / len(scores["hallucination"])
    saf_avg = sum(scores["safety"]) / len(scores["safety"])
    print(f"{section}: Accuracy {acc_avg:.2f}, Hallucination {hal_avg:.2f}, Safety {saf_avg:.2f}")

    # ============================
# 🔹 FINAL CODECOACH SCORE
# ============================
all_scores = {"accuracy": [], "hallucination": [], "safety": []}

# Collect all scores across all sections
for scores in section_scores.values():
    all_scores["accuracy"].extend(scores["accuracy"])
    all_scores["hallucination"].extend(scores["hallucination"])
    all_scores["safety"].extend(scores["safety"])

# Compute average scores
avg_accuracy = sum(all_scores["accuracy"]) / len(all_scores["accuracy"])
avg_hallucination = sum(all_scores["hallucination"]) / len(all_scores["hallucination"])
avg_safety = sum(all_scores["safety"]) / len(all_scores["safety"])

# Combine into final score (hallucination is inverse)
final_score = ((avg_accuracy + (1 - avg_hallucination) + avg_safety) / 3) * 100

print("\n=== FINAL CODECOACH SCORE ===")
print(f"Combined Score: {final_score:.2f}%")


# Combine all scores
all_scores = {"accuracy": [], "hallucination": [], "safety": []}
for section, scores in section_scores.items():
    all_scores["accuracy"].extend(scores["accuracy"])
    all_scores["hallucination"].extend(scores["hallucination"])
    all_scores["safety"].extend(scores["safety"])

# Avoid division by zero
if len(all_scores["accuracy"]) == 0:
    print("⚠️ No scores calculated because no API responses were received.")
    final_score = 0
else:
    avg_accuracy = sum(all_scores["accuracy"]) / len(all_scores["accuracy"])
    avg_hallucination = 1 - (sum(all_scores["hallucination"]) / len(all_scores["hallucination"]))
    avg_safety = sum(all_scores["safety"]) / len(all_scores["safety"])

    final_score = (avg_accuracy + avg_hallucination + avg_safety) / 3 * 100
    print(f"\n✅ Final CodeCoach Score: {final_score:.2f}%")



    # ============================
# 🔹 LOG FINAL SCORE TO LANGFUSE
# ============================

# Create a summary trace
final_trace_payload = {
    "name": "codecoach-final-score",
    "input": "All evaluation results combined",
    "output": f"Final CodeCoach Score: {final_score:.2f}%",
    "metadata": {
        "total_questions": len(test_prompts),
        "sections": list(section_scores.keys())
    }
}

trace_resp = requests.post(f"{LANGFUSE_BASE_URL}/traces", headers=headers, data=json.dumps(final_trace_payload))

if trace_resp.status_code == 200:
    final_trace_id = trace_resp.json().get("id")
    # Log the final combined score
    score_payload = {"traceId": final_trace_id, "name": "final_score", "value": final_score / 100}
    requests.post(f"{LANGFUSE_BASE_URL}/scores", headers=headers, data=json.dumps(score_payload))
    print("✅ Final score logged to Langfuse!")
else:
    print(f"❌ Could not log final score: {trace_resp.status_code} {trace_resp.text}")



