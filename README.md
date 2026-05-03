# AgentEval: A Benchmark Framework for Evaluating Agentic AI Systems in Real-World Tasks


[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Groq](https://img.shields.io/badge/API-Groq%20Free-orange.svg)](https://console.groq.com)
[![Ollama](https://img.shields.io/badge/Local-Ollama-purple.svg)](https://ollama.com)

> **Author:** Md Fahim Muntasir  
> **Institution:** Bangladesh Army International University of Science and Technology (BAIUST), Bangladesh  
> **Email:** fahimmuntasir321@gmail.com  
> **Paper:** [arXiv link — update after submission]

---

## Overview

**AgentEval** is a multi-dimensional benchmark framework for evaluating large language model (LLM) based autonomous agents across realistic, open-ended tasks. Unlike existing benchmarks that rely on single metrics such as accuracy or pass rate, AgentEval measures agent performance across **five independent dimensions**:

| Dimension | Sub-metrics | What it measures |
|---|---|---|
| **Task Success** | Completion Rate (CR), Output Accuracy (OA) | Whether the agent achieves the goal |
| **Efficiency** | Step Count (SC), Time to Completion (TTC) | Cost of achieving the goal |
| **Tool Usage** | Tool Selection Accuracy (TSA), Execution Success (TESR) | Quality of tool/strategy selection |
| **Reasoning Quality** | Logical Consistency (LC), Multi-Step Coherence (MSC) | Coherence of the reasoning process |
| **Robustness** | Noisy Input Performance (NIP), Error Recovery Rate (ERR) | Resilience under imperfect conditions |

---

## Key Results

Experiments comparing **LLaMA-3.1-8B-Instant** (Groq API) and **TinyLLaMA-1.1B** (Ollama, local) on 20 benchmark tasks:

| Category | LLaMA-3.1 CR | TinyLLaMA CR | Gap |
|---|---|---|---|
| Multi-step Reasoning | 0.600 | 0.200 | 0.400 |
| Question Answering | 1.000 | 0.800 | 0.200 |
| **Coding** | **1.000** | **1.000** | **0.000** |
| Robustness | 1.000 | 0.400 | 0.600 |
| **Overall** | **0.900** | **0.600** | **0.300** |

**Key finding:** Both agents achieve identical perfect scores on Coding tasks — showing that structured, well-specified tasks narrow the gap between large and small models.

---

## Project Structure

```
agenteval/
├── run_experiment_free.py   # Main experiment runner (zero cost)
├── results.xlsx             # Full experimental results (auto-generated)
├── paper/
│   ├── agenteval.tex        # arXiv-ready LaTeX source
│   └── agenteval.pdf        # Compiled paper
├── .env.example             # API key template (copy to .env)
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- A free [Groq API key](https://console.groq.com) (no credit card required)

### 1. Clone the repository

```bash
git clone https://github.com/fahimmuntasir321/agenteval.git
cd agenteval
```

### 2. Install dependencies

```bash
pip install groq ollama pandas openpyxl
```

### 3. Download TinyLLaMA (runs locally, free)

```bash
ollama pull tinyllama
```

### 4. Set up your API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free key at [console.groq.com](https://console.groq.com) — no credit card needed.

### 5. Run the experiments

```bash
python run_experiment_free.py
```

Results are automatically saved to `results.xlsx` with two sheets:
- **Summary** — aggregate scores per category (copy into your paper)
- **All Results** — full response traces for every task

---

## Benchmark Tasks

The benchmark contains **20 tasks** across 4 categories × 3 difficulty levels:

| Category | Tasks | Difficulties | Example |
|---|---|---|---|
| Multi-step Reasoning | 5 | Easy / Medium / Hard | Pipe filling rate problem |
| Question Answering | 5 | Easy / Medium / Hard | Capital city, ML concepts |
| Coding | 5 | Easy / Medium / Hard | Palindrome, binary search |
| Robustness | 5 | Easy / Medium / Hard | Misspelled arithmetic questions |

---

## Agents Evaluated

| | LLaMA-3.1-8B-Instant | TinyLLaMA-1.1B |
|---|---|---|
| **Access** | Groq free API | Local via Ollama |
| **Parameters** | 8 billion | 1.1 billion |
| **Hardware** | Groq inference chip | Consumer laptop (3.3 GB RAM) |
| **Avg. response time** | 0.66 s | 8.16 s |
| **Cost** | Free | Free |

---

## How to Cite

If you use AgentEval in your research, please cite:

```bibtex
@misc{muntasir2026agenteval,
  title   = {A Benchmark Framework for Evaluating Agentic AI Systems in Real-World Tasks},
  author  = {Muntasir, Md Fahim},
  year    = {2026},
  eprint  = {2026.XXXXX},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AI},
  url     = {https://arxiv.org/abs/2026.XXXXX}
}
```

*(Update the arXiv ID after submission)*

---

## Reproducing the Results

All steps to fully reproduce the paper results:

```bash
# 1. Install dependencies
pip install groq ollama pandas openpyxl

# 2. Pull TinyLLaMA
ollama pull tinyllama

# 3. Set API key in .env file

# 4. Run experiment
python run_experiment_free.py

# 5. Open results.xlsx — Summary sheet matches Table 5-7 in the paper
```

Total runtime: approximately 5–10 minutes on a standard consumer laptop.

---

## Contributing

Contributions are welcome. To add new task categories, additional agents, or improved scoring methods:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-tasks`
3. Commit your changes: `git commit -m 'Add domain-specific tasks'`
4. Push and open a Pull Request

---

## License

This project is released under the [MIT License](LICENSE). The benchmark tasks, evaluation code, and results are freely available for research and educational use.

---

## Contact

**Md Fahim Muntasir**  
Bangladesh Army International University of Science and Technology (BAIUST)  
📧 fahimmuntasir321@gmail.com  
🔗 GitHub: [github.com/fahimmuntasir321](https://github.com/fahim-fm)
