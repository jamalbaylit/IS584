import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from collections import Counter
import re


matplotlib.use("TkAgg")

# Set Seaborn theme
sns.set(style="whitegrid")

# Load JSONL file
print("🔹 Loading dataset...")
df = pd.read_json("dataset/processed.jsonl", lines=True)
print(f"✅ Dataset loaded. Total entries: {len(df)}")

# Show sample
print("\n🔹 Sample of dataset:")
print(df.head(3))

# Add word and character count columns
print("\n🔹 Calculating word and character counts...")
df["title_word_count"] = df["title"].str.split().str.len()
df["abstract_word_count"] = df["abstract"].str.split().str.len()
df["title_char_count"] = df["title"].str.len()
df["abstract_char_count"] = df["abstract"].str.len()

# Descriptive stats
print("\n📊 Descriptive Statistics:")
print(df[["title_word_count", "abstract_word_count", "title_char_count", "abstract_char_count"]].describe())



# 1. Distribution of abstract word count
plt.figure(figsize=(12, 6))
sns.histplot(df["abstract_word_count"], bins=50, kde=True, color="skyblue")
plt.title("Distribution of Abstract Word Count", fontsize=16)
plt.xlabel("Abstract Word Count")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()


# 1. Distribution of  word count
plt.figure(figsize=(12, 6))
sns.histplot(df["title_word_count"], bins=50, kde=True, color="skyblue")
plt.title("Distribution of Title Word Count", fontsize=16)
plt.xlabel("Title Word Count")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# # 2. Title vs Abstract word count
# plt.figure(figsize=(8, 6))
# sns.scatterplot(x="title_word_count", y="abstract_word_count", data=df, alpha=0.6)
# plt.title("Title vs Abstract Word Count", fontsize=16)
# plt.xlabel("Title Word Count")
# plt.ylabel("Abstract Word Count")
# plt.tight_layout()
# plt.show()

# 3. Top 20 words in abstract
def get_top_words(series, n=20):
    text = " ".join(series.dropna()).lower()
    words = re.findall(r'\b\w+\b', text)
    return Counter(words).most_common(n)

top_words_abstract = get_top_words(df["abstract"])
top_words_title = get_top_words(df["title"])

words, freqs = zip(*top_words_abstract)
plt.figure(figsize=(12, 6))
sns.barplot(x=list(freqs), y=list(words), palette="viridis")
plt.title("Top 20 Words in Abstract Text", fontsize=16)
plt.xlabel("Frequency")
plt.ylabel("Word")
plt.tight_layout()
plt.show()


words, freqs = zip(*top_words_title)
plt.figure(figsize=(12, 6))
sns.barplot(x=list(freqs), y=list(words), palette="viridis")
plt.title("Top 20 Words in Title Text", fontsize=16)
plt.xlabel("Frequency")
plt.ylabel("Word")
plt.tight_layout()
plt.show()

# # 4. Heatmap of correlation between word/char counts
# plt.figure(figsize=(8, 6))
# corr = df[["title_word_count", "abstract_word_count", "title_char_count", "abstract_char_count"]].corr()
# sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
# plt.title("Correlation Heatmap", fontsize=14)
# plt.tight_layout()
# plt.show()

# Optional: print top title lengths
print("\n🔹 Longest Titles:")
print(df[["title", "title_word_count"]].sort_values(by="title_word_count", ascending=False).head(5))

print("\n🔹 Longest Bodies:")
print(df[["abstract", "abstract_word_count"]].sort_values(by="abstract_word_count", ascending=False).head(3))
