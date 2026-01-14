import csv
import time
import os
import sys

# --- LIBRARIES ---
try:
    import openai
    import anthropic
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
except ImportError as e:
    print(f"CRITICAL ERROR: Missing library. {e}")
    print("Run: pip install openai anthropic google-generativeai")
    sys.exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================

# 1. MODELS TO RUN (The script will loop through this list)
# It uses the "Mini/Fast" versions as requested for execution.
MODELS_TO_RUN = [
    "gpt-4o-mini",  # OpenAI
    "claude-3-haiku-20240307",  # Anthropic
    "gemini-2.5-flash"  # Google
]

# 2. SAFETY SWITCH
# Set to True to test (runs 3 prompts per model).
# Set to False to run ALL 1250 prompts per model.
DRY_RUN = False

# 3. API KEYS
KEYS = {
    "openai": "YOUR_API_KEY",
    "anthropic": "YOUR_API_KEY",
    "google": "YOUR_API_KEY"
}

# 4. INPUT FILE
INPUT_FILENAME = "financial_injection_benchmark_unified.csv"


# =============================================================================
# ENGINE SWITCHING LOGIC
# =============================================================================
class ModelWrapper:
    def __init__(self, model_name, keys):
        self.model_name = model_name
        self.provider = ""

        if "gpt" in model_name.lower() or "o1-" in model_name.lower():
            self.provider = "openai"
            if not keys["openai"]: raise ValueError("Missing OpenAI Key")
            self.client = openai.OpenAI(api_key=keys["openai"])

        elif "claude" in model_name.lower():
            self.provider = "anthropic"
            if not keys["anthropic"]: raise ValueError("Missing Anthropic Key")
            self.client = anthropic.Anthropic(api_key=keys["anthropic"])

        elif "gemini" in model_name.lower():
            self.provider = "google"
            if not keys["google"]: raise ValueError("Missing Google Key")
            genai.configure(api_key=keys["google"])
            self.model = genai.GenerativeModel(model_name)

        else:
            raise ValueError(f"Unknown Model: {model_name}")

    def generate(self, prompt):
        try:
            # --- OPENAI ---
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    max_tokens=2000
                )
                return response.choices[0].message.content.strip()

            # --- ANTHROPIC ---
            elif self.provider == "anthropic":
                message = self.client.messages.create(
                    model=self.model_name,
                    max_tokens=2000,
                    temperature=0.0,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text

            # --- GOOGLE ---
            elif self.provider == "google":
                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
                response = self.model.generate_content(
                    prompt,
                    safety_settings=safety_settings,
                    generation_config=genai.types.GenerationConfig(
                        candidate_count=1,
                        max_output_tokens=2000,
                        temperature=0.0
                    )
                )
                return response.text.strip()

        except Exception as e:
            return f"ERROR_API: {str(e)}"


# =============================================================================
# MAIN PIPELINE
# =============================================================================
def run_all_models():
    if not os.path.exists(INPUT_FILENAME):
        print(f"Error: {INPUT_FILENAME} not found.")
        return

    # Read Input Data Once
    with open(INPUT_FILENAME, 'r', encoding='utf-8') as infile:
        raw_data = list(csv.DictReader(infile))
        fieldnames = raw_data[0].keys() if raw_data else []
        full_fieldnames = list(fieldnames) + ['Model_Response', 'Model_Name']

    print(f"\n--- BATCH EXECUTION STARTED ---")
    print(f"Models to run: {MODELS_TO_RUN}")
    print(f"Mode: {'DRY RUN (3 prompts each)' if DRY_RUN else 'FULL RUN (1250 prompts each)'}")

    # --- LOOP THROUGH EACH MODEL ---
    for model_name in MODELS_TO_RUN:
        print(f"\n>>> STARTING MODEL: {model_name}")

        try:
            engine = ModelWrapper(model_name, KEYS)
        except ValueError as e:
            print(f"Skipping {model_name}: {e}")
            continue

        output_filename = f"financial_results_{model_name}.csv"

        # Open specific output file for this model
        with open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=full_fieldnames)
            writer.writeheader()

            count = 0
            total = len(raw_data)

            for row in raw_data:
                count += 1
                if count % 10 == 0:
                    print(f"   [{model_name}] Processing {count}/{total}...")

                # Generate
                response = engine.generate(row['Full_Prompt'])

                # Save
                row['Model_Response'] = response
                row['Model_Name'] = model_name
                writer.writerow(row)
                outfile.flush()

                if DRY_RUN and count >= 3:
                    print(f"   --- Dry Run limit reached for {model_name} ---")
                    break

                # Rate limit sleep
                time.sleep(0.2)

        print(f">>> FINISHED {model_name}. Saved to {output_filename}")

    print("\n--- ALL MODELS COMPLETE ---")


if __name__ == "__main__":
    run_all_models()
