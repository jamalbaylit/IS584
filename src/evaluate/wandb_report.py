import wandb
import pandas as pd
import matplotlib.pyplot as plt

# Initialize
wandb.init(project="RAG-Retrieval-Study", name="Method-Evaluation", config={
    "dataset": "synthetic_academic_260",
    "embedding_model": "DistilBERT"
})

# Log local dataset as artifact
artifact = wandb.Artifact("synthetic_academic_260", type="dataset")
artifact.add_file("./dataset/processed.jsonl")
wandb.log_artifact(artifact)

# Read and log a sample
df = pd.read_json("./dataset/processed.jsonl", lines=True)
wandb.log({"Sample Data": wandb.Table(dataframe=df.head(10))})

# Accuracy log
from src.evaluate.benchmark import main
results = main()
for method, acc in results.items():
    wandb.log({f"{method} Accuracy": acc})

# Plot
methods, accs = list(results.keys()), list(results.values())
plt.figure(figsize=(8, 5))
plt.barh(methods, accs)
plt.xlabel("Accuracy (%)")
plt.title("Method Performance")
wandb.log({"Accuracy Plot": wandb.Image(plt)})

wandb.finish()
