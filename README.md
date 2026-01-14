Assistant or Adversary?
Auditing Financial LLMs Against Indirect Prompt Injection

This repository contains the dataset, codebase, and evaluation results for the academic study:

Assistant or Adversary? Auditing Financial LLMs Against Indirect Prompt Injection

The project introduces a domain-specific benchmark designed to evaluate the robustness of large language models (LLMs) against Indirect Prompt Injection (IPI) attacks in high-stakes financial contexts.

📌 Overview

Total attack instances: 1,250

Financial domains: 10 high-risk niches (e.g., Insider Trading, Payroll, Strategic Planning)

Models evaluated:

GPT-4o-mini

Claude-3-Haiku

Gemini-2.5-Flash

The benchmark systematically measures attack success rates (ASR) and information leakage severity across models, domains, and attack vectors.

📂 Repository Structure

The repository is organized to ensure full reproducibility of the experimental pipeline, from attack generation to final visualization.

financial-ipi-benchmark/
├── assets/
│ ├── figures/ # Visualization figures used in the paper
│ └── paper.pdf # Final academic thesis PDF
│
├── data/
│ ├── benchmark_dataset/
│ │ └── financial_injection_benchmark_unified.csv
│ │ # Unified dataset of 1,250 adversarial prompts
│ ├── input/
│ │ └── UNIFIED FINANCIAL CONTEXT ARCHIVE.docx
│ │ # Source text for the 10 financial carrier documents
│ └── results/
│ ├── graded_by_llm/ # LLM-as-a-Judge evaluation logs
│ ├── raw_responses/ # Raw JSON/CSV outputs from model APIs
│ └── final_benchmark_summary.csv
│ # Aggregated metrics (ASR, Severity)
│
├── scripts/ # Python scripts for the experimental pipeline
├── .gitignore # Security and exclusion configuration
├── README.md # Project documentation
└── requirements.txt # Python dependencies

🚀 Key Findings

Our evaluation across 1,250 indirect prompt injection attacks reveals notable security gaps in financial LLM deployments:

🔓 Model Vulnerability

GPT-4o-mini showed the highest susceptibility

60.4% Attack Success Rate (ASR)

Frequently prioritized embedded instructions over safety constraints

🛡️ Model Robustness

Claude-3-Haiku was the most resilient

26.5% ASR

Demonstrated consistent refusal and constraint adherence

⚠️ High-Risk Contexts

Future Strategy & Planning documents were the most vulnerable

61.1% average ASR

Role Impersonation attacks (e.g., “I am the CEO”) were the most effective attack vector

🛠️ Reproduction Pipeline

Follow the steps below to fully reproduce the benchmark results.

1️⃣ Attack Generation

Generates 1,250 adversarial prompts by combining:

10 financial carrier documents

5 attack vectors

5 obfuscation strategies

Script: scripts/creating_ipi_attacks.py

Output:
data/benchmark_dataset/financial_injection_benchmark_unified.csv

2️⃣ Model Execution

Executes the generated prompts against the target model APIs.

Script: scripts/execution_code.py

Output directory:
data/results/raw_responses/

Requires valid API keys for OpenAI, Anthropic, and Google.

3️⃣ Evaluation (LLM-as-a-Judge)

Grades each model response for:

Attack success (ASR)

Information leakage severity

Evaluation combines an independent LLM with regex-based parsers.

Script: scripts/evaluate_results.py

Output directory:
data/results/graded_by_llm/

4️⃣ Summarization

Aggregates graded evaluations into final benchmark metrics.

Script: scripts/creating_summary.py

Output:
data/results/final_benchmark_summary.csv

5️⃣ Visualization

Generates the figures used in the paper (heatmaps and bar charts).

Script: scripts/generating_plots_from_benchmark_summary.py

Output directory:
assets/figures/

⚙️ Installation
Clone the Repository
git clone https://github.com/YOUR_USERNAME/financial-ipi-benchmark.git
cd financial-ipi-benchmark

Install Dependencies
pip install -r requirements.txt

Environment Setup

Set your API keys as environment variables (or via a local secrets file) before running:

execution_code.py

📜 License & Usage

This project is intended strictly for academic and research purposes.

If you plan to reuse the dataset, benchmark design, or evaluation methodology, please cite the associated paper.
