import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from textwrap import wrap

# ---------------------------------------------------------
# 1. SETUP & DATA LOADING
# ---------------------------------------------------------
df = pd.read_csv('final_benchmark_summary.csv')

df = df.rename(columns={
    'Niche': 'Financial_Niche',
    'Final_ASR': 'Attack_Success',
    'LLM_Severity': 'Leakage_Severity_Score',
    'LLM_RQS': 'Refusal_Quality_Score'
})


def get_detection_source(row):
    regex = row['Regex_Detected']
    llm_detect = row['LLM_ASR']
    if regex and llm_detect:
        return 'Detected by Both'
    elif regex and not llm_detect:
        return 'Regex Only (Literal)'
    elif not regex and llm_detect:
        return 'Judge Only (Semantic)'
    return 'Not Detected'


df['Detection_Source'] = df.apply(get_detection_source, axis=1)

model_order = ['claude-3-haiku-20240307', 'gemini-2.5-flash', 'gpt-4o-mini']
palette = {'claude-3-haiku-20240307': '#4E598C', 'gemini-2.5-flash': '#2E8B7E', 'gpt-4o-mini': '#76C06E'}
sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.figsize': (10, 6), 'figure.dpi': 150})


def save_plot(filename):
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Saved {filename}")


# ---------------------------------------------------------
# 2. PLOTTING FUNCTIONS (Renumbered 1-10)
# ---------------------------------------------------------

# FIGURE 1: Comparative Vulnerability (ASR) Across Models
def plot_fig_1(data):
    plt.figure()
    asr_data = data.groupby('Model_Name')['Attack_Success'].mean().reset_index()
    ax = sns.barplot(data=asr_data, x='Model_Name', y='Attack_Success', order=model_order, palette=palette,
                     hue='Model_Name', legend=False)
    plt.title("Figure 1: Comparative Vulnerability (ASR) Across Models", fontsize=14)
    plt.ylabel("Attack Success Rate (ASR)")
    plt.xlabel("Model Family")
    plt.ylim(0, 1.0)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3)
    save_plot("Figure_1_Overall_ASR.png")


# FIGURE 2: Heatmap of Attack Success Rate by Financial Niche
def plot_fig_2(data):
    plt.figure(figsize=(10, 8))
    pivot = data.pivot_table(index='Financial_Niche', columns='Model_Name', values='Attack_Success', aggfunc='mean')
    sns.heatmap(pivot, annot=True, cmap="Reds", fmt=".2f", vmin=0, vmax=1)
    plt.title("Figure 2: Heatmap of Attack Success Rate by Financial Niche", fontsize=14)
    plt.xlabel("Model")
    plt.ylabel("Financial Niche")
    save_plot("Figure_2_Niche_Frequency_Heatmap.png")


# FIGURE 3: Attack Success Rate (ASR) per Financial Niche by Model (Bar Chart)
def plot_fig_3(data):
    plt.figure(figsize=(14, 7))
    sns.barplot(data=data, x='Financial_Niche', y='Attack_Success', hue='Model_Name', errorbar=None, palette=palette,
                hue_order=model_order)
    plt.title("Figure 3: Attack Success Rate (ASR) per Financial Niche by Model", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Attack Success Rate (%)")
    plt.legend(title='Model')
    save_plot("Figure_3_Niche_Breakdown_Bars.png")


# FIGURE 4: Heatmap of Average Leakage Severity (1-5)
def plot_fig_4(data):
    plt.figure(figsize=(10, 8))
    pivot = data.pivot_table(index='Financial_Niche', columns='Model_Name', values='Leakage_Severity_Score',
                             aggfunc='mean')
    sns.heatmap(pivot, annot=True, cmap="Oranges", fmt=".2f", vmin=1, vmax=5)
    plt.title("Figure 4: Heatmap of Average Leakage Severity (1-5)", fontsize=14)
    plt.xlabel("Model")
    plt.ylabel("Financial Niche")
    save_plot("Figure_4_Severity_Heatmap.png")


# FIGURE 5: Attack Effectiveness by Approach Strategy
def plot_fig_5(data):
    plt.figure(figsize=(12, 6))
    sns.barplot(data=data, x='Attack_Approach', y='Attack_Success', hue='Model_Name', errorbar=None, palette=palette,
                hue_order=model_order)
    plt.title("Figure 5: Attack Effectiveness by Approach Strategy", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Attack Success Rate (ASR)")
    save_plot("Figure_5_Vector_Strategy.png")


# FIGURE 6: Impact of Textual Variation/Obfuscation on ASR
def plot_fig_6(data):
    plt.figure(figsize=(12, 6))
    sns.barplot(data=data, x='Textual_Variation', y='Attack_Success', hue='Model_Name', errorbar=None, palette=palette,
                hue_order=model_order)
    plt.title("Figure 6: Impact of Textual Variation/Obfuscation on ASR", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Attack Success Rate (ASR)")
    save_plot("Figure_6_Obfuscation.png")


# FIGURE 7: Impact of Prompt Template (Task Framing) on ASR (MOVED HERE)
def plot_fig_7(data):
    plt.figure(figsize=(14, 8))
    asr_data = data.groupby(['Prompt_Template', 'Model_Name'])['Attack_Success'].mean().reset_index()
    template_order = data.groupby('Prompt_Template')['Attack_Success'].mean().sort_values(ascending=False).index

    ax = sns.barplot(data=asr_data, x='Prompt_Template', y='Attack_Success', hue='Model_Name', palette=palette,
                     hue_order=model_order, order=template_order)

    plt.title("Figure 7: Impact of Prompt Template (Task Framing) on ASR", fontsize=14)
    plt.ylabel("Attack Success Rate (ASR)")
    plt.xlabel("Task Framing (Prompt Template)")
    plt.ylim(0, 1.0)

    labels = ['\n'.join(wrap(label, 30)) for label in template_order]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=0, fontsize=9)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3, fontsize=8)
    save_plot("Figure_7_Prompt_Templates.png")


# FIGURE 8: Severity Distribution of Successful Attacks (Moved from Fig 6)
def plot_fig_8(data):
    plt.figure()
    leaks = data[data['Leakage_Severity_Score'] > 1]
    sns.countplot(data=leaks, x='Leakage_Severity_Score', hue='Model_Name', palette=palette, hue_order=model_order)
    plt.title("Figure 8: Severity Distribution of Successful Attacks (Severity > 1)", fontsize=14)
    plt.xlabel("Leakage Severity Score (2-5)")
    plt.ylabel("Count of Instances")
    save_plot("Figure_8_Severity_Dist.png")


# FIGURE 9: Refusal Quality Score (RQS) Distribution (Moved from Fig 7)
def plot_fig_9(data):
    plt.figure()
    sns.countplot(data=data, x='Refusal_Quality_Score', hue='Model_Name', palette=palette, hue_order=model_order)
    plt.title("Figure 9: Refusal Quality Score (RQS) Distribution", fontsize=14)
    plt.xlabel("RQS (1=Poor, 2=Partial, 3=Robust)")
    plt.ylabel("Count")
    save_plot("Figure_9_RQS_Dist.png")


# FIGURE 10: Contribution of Detection Methods (Moved from Fig 8/9)
def plot_fig_10(data):
    plt.figure()
    successful = data[data['Attack_Success'] == 1]
    det_palette = {'Regex Only (Literal)': '#440154', 'Detected by Both': '#21908d', 'Judge Only (Semantic)': '#fde725'}
    det_order = ['Regex Only (Literal)', 'Detected by Both', 'Judge Only (Semantic)']

    sns.countplot(data=successful, x='Model_Name', hue='Detection_Source', order=model_order, hue_order=det_order,
                  palette=det_palette)
    plt.title("Figure 10: Contribution of Detection Methods (Regex vs. Judge)", fontsize=14)
    plt.xlabel("Model")
    plt.ylabel("Count of Detected Attacks")
    save_plot("Figure_10_Detection_Methods.png")


if __name__ == "__main__":
    plot_fig_1(df)
    plot_fig_2(df)
    plot_fig_3(df)
    plot_fig_4(df)
    plot_fig_5(df)
    plot_fig_6(df)
    plot_fig_7(df)
    plot_fig_8(df)
    plot_fig_9(df)
    plot_fig_10(df)
    print("All 10 figures generated successfully in the correct order.")
