"""
AgentEval Experiment Runner — COMPLETELY FREE VERSION
======================================================
Agent 1: LLaMA-3.1-8B   via Groq  (free API, no credit card)
Agent 2: TinyLLaMA-1.1B via Ollama (runs locally on your PC, free)

SETUP (do this once):
1. Go to https://console.groq.com → sign up free → API Keys → Create Key
2. Download Ollama from https://ollama.com and install it
3. Open VS Code terminal and run:  ollama pull tinyllama
4. In VS Code terminal run:  pip install groq ollama pandas openpyxl
5. Create a file called .env in this folder and write inside:
      GROQ_API_KEY=your_key_here

HOW TO RUN:
   Press F5 in VS Code   OR   type in terminal:
   python run_experiment_free.py

WHAT HAPPENS:
   Both agents answer all 20 tasks.
   Results are saved to results.xlsx
   Copy the numbers from the Summary sheet into your paper!
"""

import os
import time
import pandas as pd
from datetime import datetime

# ── Load .env file ────────────────────────────────────────────────────────────
def load_env():
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env()

# ── Check packages ────────────────────────────────────────────────────────────
try:
    from groq import Groq
except ImportError:
    print("\nERROR: Missing packages. Run this in your terminal:")
    print("   pip install groq ollama pandas openpyxl\n")
    exit()

try:
    import ollama as ollama_client
except ImportError:
    print("\nERROR: Missing packages. Run this in your terminal:")
    print("   pip install groq ollama pandas openpyxl\n")
    exit()

# ── 20 Benchmark Tasks ────────────────────────────────────────────────────────
TASKS = [

    # ── Category 1: Multi-step Reasoning ─────────────────────────────────────
    {
        "id": "R01", "category": "Multi-step Reasoning", "difficulty": "Easy",
        "question": "A store sells apples for $1.20 each and oranges for $0.80 each. "
                    "Sarah buys 5 apples and 3 oranges. How much does she spend in total?",
        "success_keywords": ["8.40", "$8.40", "8 dollars"]
    },
    {
        "id": "R02", "category": "Multi-step Reasoning", "difficulty": "Easy",
        "question": "A train travels 120 km in 2 hours, then 180 km in 3 hours. "
                    "What is the average speed for the entire journey?",
        "success_keywords": ["60", "60 km/h", "60km/h"]
    },
    {
        "id": "R03", "category": "Multi-step Reasoning", "difficulty": "Medium",
        "question": "A company has 240 employees. 25% are in engineering, 35% in sales, "
                    "the rest in operations. Engineering hires 20 more people. "
                    "What percentage of total staff is engineering now?",
        "success_keywords": ["29", "30", "29.6", "29.5"]
    },
    {
        "id": "R04", "category": "Multi-step Reasoning", "difficulty": "Medium",
        "question": "Pipe A fills a tank in 4 hours. Pipe B drains it in 6 hours. "
                    "Both are open and the tank starts empty. "
                    "How many hours does it take to fill the tank completely?",
        "success_keywords": ["12", "twelve", "12 hours"]
    },
    {
        "id": "R05", "category": "Multi-step Reasoning", "difficulty": "Hard",
        "question": "Three friends split a restaurant bill. Alice paid $45, Bob paid $30, "
                    "Carol paid $25. They agreed to split evenly. "
                    "How much does Bob owe Alice, and how much does Carol owe Alice?",
        "success_keywords": ["3.33", "8.33", "3 dollars", "8 dollars"]
    },

    # ── Category 2: Question Answering ────────────────────────────────────────
    {
        "id": "Q01", "category": "Question Answering", "difficulty": "Easy",
        "question": "What is the capital city of Australia? "
                    "Note: many people confuse this with Sydney.",
        "success_keywords": ["canberra", "Canberra"]
    },
    {
        "id": "Q02", "category": "Question Answering", "difficulty": "Easy",
        "question": "What does the abbreviation 'LLM' stand for "
                    "in the context of artificial intelligence?",
        "success_keywords": ["large language model", "Large Language Model"]
    },
    {
        "id": "Q03", "category": "Question Answering", "difficulty": "Medium",
        "question": "Explain the difference between supervised and unsupervised learning "
                    "in machine learning. Give one example of each.",
        "success_keywords": ["labeled", "label", "supervised", "unsupervised", "cluster"]
    },
    {
        "id": "Q04", "category": "Question Answering", "difficulty": "Medium",
        "question": "What is the difference between precision and recall in machine learning? "
                    "Which would you prioritise for a medical diagnosis system and why?",
        "success_keywords": ["recall", "false negative", "miss", "medical"]
    },
    {
        "id": "Q05", "category": "Question Answering", "difficulty": "Hard",
        "question": "Why can gradient descent get stuck in local minima? "
                    "What technique is commonly used to help escape local minima "
                    "in deep learning?",
        "success_keywords": ["momentum", "stochastic", "SGD", "local minima"]
    },

    # ── Category 3: Coding ────────────────────────────────────────────────────
    {
        "id": "C01", "category": "Coding", "difficulty": "Easy",
        "question": "Write a Python function called 'is_palindrome' that takes a string "
                    "and returns True if it is a palindrome, False otherwise. "
                    "Test it with 'racecar' and 'hello'.",
        "success_keywords": ["def is_palindrome", "True", "False", "racecar"]
    },
    {
        "id": "C02", "category": "Coding", "difficulty": "Easy",
        "question": "Write a Python function 'count_words' that counts the number of words "
                    "in a string. Test it with: 'The quick brown fox jumps over the lazy dog'",
        "success_keywords": ["def count_words", "split", "9"]
    },
    {
        "id": "C03", "category": "Coding", "difficulty": "Medium",
        "question": "Write a Python function 'find_duplicates' that takes a list of integers "
                    "and returns a list of numbers that appear more than once. "
                    "Test it with [1, 2, 3, 2, 4, 3, 5].",
        "success_keywords": ["def find_duplicates", "2", "3", "duplicate"]
    },
    {
        "id": "C04", "category": "Coding", "difficulty": "Medium",
        "question": "Write a Python class 'Stack' with push, pop, peek, and is_empty methods. "
                    "Show how to use it to reverse the string 'hello'.",
        "success_keywords": ["class Stack", "def push", "def pop", "olleh"]
    },
    {
        "id": "C05", "category": "Coding", "difficulty": "Hard",
        "question": "Write a Python function 'binary_search' that searches for a target "
                    "in a sorted list and returns its index, or -1 if not found. "
                    "Test with the list [1,3,5,7,9,11,13] searching for 7.",
        "success_keywords": ["def binary_search", "mid", "3"]
    },

    # ── Category 4: Robustness (noisy/messy inputs) ───────────────────────────
    {
        "id": "N01", "category": "Robustness", "difficulty": "Easy",
        "question": "wat is 15 persent of 200?? i need this 4 my homework lol",
        "success_keywords": ["30", "thirty"]
    },
    {
        "id": "N02", "category": "Robustness", "difficulty": "Easy",
        "question": "the thing darwin wrote about.. how does it work agian? naturel selction?",
        "success_keywords": ["natural selection", "survival", "evolut"]
    },
    {
        "id": "N03", "category": "Robustness", "difficulty": "Medium",
        "question": "i have 3 cats and my friend has double that minus one "
                    "how many cats total between us???",
        "success_keywords": ["8", "eight"]
    },
    {
        "id": "N04", "category": "Robustness", "difficulty": "Medium",
        "question": "Explin difrence btween RAM and ROM in computr? i always get confusd",
        "success_keywords": ["RAM", "ROM", "temporary", "permanent", "volatile"]
    },
    {
        "id": "N05", "category": "Robustness", "difficulty": "Hard",
        "question": "if a train leaves at 9am going 60mph and another leaves same station "
                    "30min later going 90mph wen do they meet??? same track same direction",
        "success_keywords": ["10:30", "90 miles", "1.5 hours", "1 hour 30"]
    },
]

# ── Scoring helpers ───────────────────────────────────────────────────────────

def score_success(response, task):
    """Return 1 if response contains any expected keyword, else 0."""
    r = response.lower()
    return 1 if any(k.lower() in r for k in task["success_keywords"]) else 0

def count_steps(response):
    """Estimate reasoning steps from structure in the response."""
    lines = [l.strip() for l in response.split('\n') if l.strip()]
    indicators = sum(
        1 for l in lines if l and (
            l[0].isdigit() or
            l.startswith(('-', '*', '•')) or
            any(l.startswith(w) for w in ['Step', 'First', 'Then', 'Next', 'Finally'])
        )
    )
    return max(1, indicators)

def lc_score(response):
    """Estimate logical consistency score (1-5) from response length and structure."""
    words = len(response.split())
    structured = any(w in response for w in
                     ['1.', '2.', 'First', 'Then', 'Therefore',
                      'Because', 'Since', 'Step'])
    if words > 150 and structured:
        return 4.5
    elif words > 80 and structured:
        return 3.5
    elif words > 40:
        return 3.0
    else:
        return 2.0

# ── Agent 1: LLaMA-3.1-8B via Groq (FREE) ────────────────────────────────────

def run_groq_agent(task):
    """Run LLaMA-3.1-8B on Groq free API."""
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return {
            "success": 0, "time_seconds": 0, "steps": 0, "lc": 0,
            "response": "ERROR: No GROQ_API_KEY found in .env file"
        }
    try:
        client = Groq(api_key=api_key)
        t0 = time.time()
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. "
                               "Answer clearly and show your reasoning step by step."
                },
                {
                    "role": "user",
                    "content": task["question"]
                }
            ],
            max_tokens=600,
            temperature=0.0
        )
        elapsed = round(time.time() - t0, 2)
        text = chat.choices[0].message.content
        return {
            "success":      score_success(text, task),
            "time_seconds": elapsed,
            "steps":        count_steps(text),
            "lc":           lc_score(text),
            "response":     text[:300]
        }
    except Exception as e:
        return {
            "success": 0, "time_seconds": 0, "steps": 0, "lc": 0,
            "response": f"ERROR: {str(e)}"
        }

# ── Agent 2: TinyLLaMA via Ollama (FREE, runs on your PC) ────────────────────

def run_tinyllama_agent(task):
    """Run TinyLLaMA-1.1B locally via Ollama."""
    try:
        t0 = time.time()
        resp = ollama_client.chat(
            model="tinyllama",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. "
                               "Answer clearly and show your reasoning step by step."
                },
                {
                    "role": "user",
                    "content": task["question"]
                }
            ]
        )
        elapsed = round(time.time() - t0, 2)
        text = resp['message']['content']
        return {
            "success":      score_success(text, task),
            "time_seconds": elapsed,
            "steps":        count_steps(text),
            "lc":           lc_score(text),
            "response":     text[:300]
        }
    except Exception as e:
        msg = str(e)
        if "connection" in msg.lower() or "refused" in msg.lower():
            msg = "Ollama not running — open the Ollama app first, then retry"
        return {
            "success": 0, "time_seconds": 0, "steps": 0, "lc": 0,
            "response": f"ERROR: {msg}"
        }

# ── Main experiment runner ────────────────────────────────────────────────────

def main():
    print("\n" + "=" * 60)
    print("  AgentEval — Free Experiment Runner")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("  Agent 1: LLaMA-3.1-8B (Groq)  |  Agent 2: TinyLLaMA (Ollama)")
    print("=" * 60)

    rows = []

    for i, task in enumerate(TASKS):
        print(f"\n[{i+1:02d}/{len(TASKS)}] {task['id']} | "
              f"{task['category']} | {task['difficulty']}")
        print(f"  Q: {task['question'][:65]}...")

        # --- Run Agent 1: Groq ---
        print("  → LLaMA-3.1 (Groq)   ...", end=" ", flush=True)
        g = run_groq_agent(task)
        if "ERROR" in g["response"]:
            print(f"ERROR: {g['response']}")
        else:
            status = "✓ PASS" if g["success"] else "✗ FAIL"
            print(f"{status}  ({g['time_seconds']}s)")

        time.sleep(0.5)  # avoid Groq rate limit

        # --- Run Agent 2: TinyLLaMA ---
        print("  → TinyLLaMA (Ollama) ...", end=" ", flush=True)
        t = run_tinyllama_agent(task)
        if "ERROR" in t["response"]:
            print(f"ERROR: {t['response']}")
        else:
            status = "✓ PASS" if t["success"] else "✗ FAIL"
            print(f"{status}  ({t['time_seconds']}s)")

        # --- Store row ---
        rows.append({
            "Task ID":              task["id"],
            "Category":             task["category"],
            "Difficulty":           task["difficulty"],
            "Question":             task["question"][:90] + "...",
            # Agent 1
            "LLaMA3.1 - Pass":      g["success"],
            "LLaMA3.1 - Time(s)":   g["time_seconds"],
            "LLaMA3.1 - Steps":     g["steps"],
            "LLaMA3.1 - LC(1-5)":   g["lc"],
            "LLaMA3.1 - Response":  g["response"],
            # Agent 2
            "TinyLLaMA - Pass":     t["success"],
            "TinyLLaMA - Time(s)":  t["time_seconds"],
            "TinyLLaMA - Steps":    t["steps"],
            "TinyLLaMA - LC(1-5)":  t["lc"],
            "TinyLLaMA - Response": t["response"],
        })

    # ── Build summary table ───────────────────────────────────────────────────
    df = pd.DataFrame(rows)
    summary = []

    for cat in ["Multi-step Reasoning", "Question Answering", "Coding", "Robustness"]:
        c = df[df["Category"] == cat]
        if len(c) > 0:
            summary.append({
                "Category":              cat,
                "Tasks":                 len(c),
                "LLaMA3.1 CR":           round(c["LLaMA3.1 - Pass"].mean(), 3),
                "LLaMA3.1 Avg Time(s)":  round(c["LLaMA3.1 - Time(s)"].mean(), 2),
                "LLaMA3.1 Avg Steps":    round(c["LLaMA3.1 - Steps"].mean(), 1),
                "LLaMA3.1 Avg LC":       round(c["LLaMA3.1 - LC(1-5)"].mean(), 2),
                "TinyLLaMA CR":          round(c["TinyLLaMA - Pass"].mean(), 3),
                "TinyLLaMA Avg Time(s)": round(c["TinyLLaMA - Time(s)"].mean(), 2),
                "TinyLLaMA Avg Steps":   round(c["TinyLLaMA - Steps"].mean(), 1),
                "TinyLLaMA Avg LC":      round(c["TinyLLaMA - LC(1-5)"].mean(), 2),
            })

    # Overall row
    summary.append({
        "Category":              "OVERALL",
        "Tasks":                 len(df),
        "LLaMA3.1 CR":           round(df["LLaMA3.1 - Pass"].mean(), 3),
        "LLaMA3.1 Avg Time(s)":  round(df["LLaMA3.1 - Time(s)"].mean(), 2),
        "LLaMA3.1 Avg Steps":    round(df["LLaMA3.1 - Steps"].mean(), 1),
        "LLaMA3.1 Avg LC":       round(df["LLaMA3.1 - LC(1-5)"].mean(), 2),
        "TinyLLaMA CR":          round(df["TinyLLaMA - Pass"].mean(), 3),
        "TinyLLaMA Avg Time(s)": round(df["TinyLLaMA - Time(s)"].mean(), 2),
        "TinyLLaMA Avg Steps":   round(df["TinyLLaMA - Steps"].mean(), 1),
        "TinyLLaMA Avg LC":      round(df["TinyLLaMA - LC(1-5)"].mean(), 2),
    })

    df_summary = pd.DataFrame(summary)

    # ── Save to Excel (2 sheets) ──────────────────────────────────────────────
    output_file = "results.xlsx"
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df_summary.to_excel(writer, sheet_name="Summary",     index=False)
        df.to_excel(        writer, sheet_name="All Results", index=False)

    # ── Print final summary in terminal ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("  EXPERIMENT COMPLETE — results saved to results.xlsx")
    print("=" * 60)
    print(f"\n  {'Category':<26} {'LLaMA3.1 CR':>12} {'TinyLLaMA CR':>13}")
    print("  " + "-" * 52)
    for r in summary:
        print(f"  {r['Category']:<26} {r['LLaMA3.1 CR']:>12.3f} "
              f"{r['TinyLLaMA CR']:>13.3f}")

    print("\n  ✓ Open results.xlsx in Excel to see full details.")
    print("  ✓ Copy the Summary sheet numbers into Section 7 of your paper.")
    print("  ✓ In your paper call them:")
    print("      Agent 1 = LLaMA-3.1-8B-Instant (Groq API)")
    print("      Agent 2 = TinyLLaMA-1.1B (Ollama, local)\n")


if __name__ == "__main__":
    main()
