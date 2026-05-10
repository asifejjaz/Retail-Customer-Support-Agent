import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

OUTPUT_DIR = os.path.dirname(__file__)

def generate_charts():
    # Set style
    sns.set_theme(style="whitegrid")

    # 1. Usability Scores Chart
    usability_data = pd.DataFrame({
        'Category': ['Ease of Use', 'Understood Queries', 'Relevant Info'],
        'Average Score (out of 5)': [4.6, 4.3, 4.5]
    })
    
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(x='Category', y='Average Score (out of 5)', data=usability_data, palette='Blues_d')
    plt.title('Beta User Feedback: Usability & Effectiveness', fontsize=14)
    plt.ylim(0, 5)
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'usability_chart.png'))
    plt.close()

    # 2. Emotional Tone Chart
    emotional_data = pd.DataFrame({
        'Category': ['Human-like Tone', 'Matched Tone/Emojis', 'Felt Valued'],
        'Average Score (out of 5)': [4.2, 4.8, 4.4]
    })
    
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(x='Category', y='Average Score (out of 5)', data=emotional_data, palette='flare')
    plt.title('Beta User Feedback: Emotional Tone & Empathy', fontsize=14)
    plt.ylim(0, 5)
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'emotional_tone_chart.png'))
    plt.close()

    # 3. Task Completion Pie Chart
    tasks = ['Product Search', 'Mock Order', 'Helpline Retrieval']
    completion_rates = [95, 88, 100] # Percentages
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Task Completion Rates', fontsize=16)
    
    colors = ['#4CAF50', '#F44336'] # Green for success, Red for failure
    
    for i, ax in enumerate(axes):
        success = completion_rates[i]
        fail = 100 - success
        ax.pie([success, fail], labels=['Success', 'Failed'], autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title(tasks[i])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'task_completion_chart.png'))
    plt.close()

    print(f"Charts successfully generated in {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_charts()
