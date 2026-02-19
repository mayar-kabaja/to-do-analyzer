import pandas as pd
import pickle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/cleaned_tasks.csv")
X = df["text"]
y_priority = df["priority"]
y_category = df["category"]

# Split BEFORE evaluating — 80% train, 20% test
X_train, X_test, yp_train, yp_test, yc_train, yc_test = train_test_split(
    X, y_priority, y_category, test_size=0.2, random_state=42
)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

X_test_vec = vectorizer.transform(X_test)  # only transform, never fit

with open("models/priority_model.pkl", "rb") as f:
    priority_model = pickle.load(f)
with open("models/category_model.pkl", "rb") as f:
    category_model = pickle.load(f)

priority_preds = priority_model.predict(X_test_vec)
category_preds = category_model.predict(X_test_vec)

print("📊 Evaluation Results")
print("----------------------")
print(f"Priority Model Accuracy:  {accuracy_score(yp_test, priority_preds):.2f}")
print(f"Category Model Accuracy:  {accuracy_score(yc_test, category_preds):.2f}")