# Assistant or Adversary? Auditing Financial LLMs Against Indirect Prompt Injection

This repository contains the dataset, codebase, and evaluation results for the academic study **"Assistant or Adversary? Auditing Financial LLMs Against Indirect Prompt Injection"**.

We introduce a domain-specific benchmark of **1,250 attack instances** spanning 10 high-stakes financial niches (e.g., Insider Trading, Payroll, Strategic Planning) to evaluate the robustness of state-of-the-art LLMs (GPT-4o-mini, Claude-3-Haiku, Gemini-2.5-Flash).

## 📂 Repository Structure

The project is organized to ensure full reproducibility of the pipeline, from attack generation to final visualization.

```text
financial-ipi-benchmark/
├── assets/
│   ├── figures/               # The 10 visualization figures used in the paper
│   └── paper.pdf              # The final academic thesis PDF
├── data/
│   ├── benchmark_dataset/     
│   │   └── financial_injection_benchmark_unified.csv  # The generated dataset of 1,250 adversarial prompts
│   ├── input/                 
│   │   └── UNIFIED FINANCIAL CONTEXT ARCHIVE.docx     # The source text for the 10 financial carrier documents
│   └── results/               
│       ├── graded_by_llm/     # Row-by-row logs of the "LLM-as-a-Judge" evaluation
│       ├── raw_responses/     # The raw JSON/CSV output from the Model APIs
│       └── final_benchmark_summary.csv # Aggregated metrics (ASR, Severity) used for plotting
├── scripts/                   # Python executables for the experimental pipeline
├── .gitignore                 # Security configuration
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
🚀 Key Findings
Our evaluation of 1,250 attacks across 10 financial niches revealed significant security gaps:

Vulnerability: GPT-4o-mini exhibited the highest susceptibility (60.4% ASR), often prioritizing embedded instructions over safety constraints.

Robustness: Claude-3-Haiku proved the most resilient (26.5% ASR), demonstrating stricter refusal behaviors.

High-Risk Niches: Future Strategy & Planning documents were the most vulnerable context (61.1% avg ASR), while "Role Impersonation" attacks (e.g., "I am the CEO") were the most effective vector.

🛠️ Reproduction Pipeline
To reproduce the results, execute the scripts in the following order:

1. Attack Generation
Generates the 1,250 adversarial prompts by combining the 10 carrier documents with 5 attack vectors and 5 obfuscation strategies.

Script: scripts/creating_ipi_attacks.py

Output: data/benchmark_dataset/financial_injection_benchmark_unified.csv

2. Execution
Runs the generated prompts against the target APIs (OpenAI, Anthropic, Google).

Script: scripts/execution_code.py

Output: Saves raw files to data/results/raw_responses/

3. Evaluation (LLM-as-a-Judge)
Uses an independent LLM and Regex parsers to grade the responses for success (ASR) and leakage severity.

Script: scripts/evaluate_results.py

Output: Saves graded logs to data/results/graded_by_llm/

4. Summarization
Aggregates the graded logs into a final statistical summary.

Script: scripts/creating_summary.py

Output: data/results/final_benchmark_summary.csv

5. Visualization
Generates the heatmaps and bar charts presented in the paper.

Script: scripts/generating_plots_from_benchmark_summary.py

Output: Saves images to assets/figures/

⚙️ Installation
1. Clone the repository:

Bash

git clone [https://github.com/YOUR_USERNAME/financial-ipi-benchmark.git](https://github.com/YOUR_USERNAME/financial-ipi-benchmark.git)
cd financial-ipi-benchmark
2. Install dependencies:

Bash

pip install -r requirements.txt
3. Environment Setup: Ensure you have your API keys set up in your environment variables (or local secrets file) to run execution_code.py.
