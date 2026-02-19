"""
Load trained models and predict priority + category for example tasks.
Run from ai-service: python predict.py
"""

import os
import pickle

_script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(_script_dir, "models", "vectorizer.pkl"), "rb") as f:
    vectorizer = pickle.load(f)
with open(os.path.join(_script_dir, "models", "priority_model.pkl"), "rb") as f:
    priority_model = pickle.load(f)
with open(os.path.join(_script_dir, "models", "category_model.pkl"), "rb") as f:
    category_model = pickle.load(f)

examples = [
    "Buy groceries",
    "Submit tax return by Friday",
    "Call doctor for appointment",
    "Finish React tutorial",
    "Review Q3 budget",
]

X_vec = vectorizer.transform(examples)
priority_preds = priority_model.predict(X_vec)
category_preds = category_model.predict(X_vec)

print("Predictions for 5 example tasks")
print("--------------------------------")
for task, priority, category in zip(examples, priority_preds, category_preds):
    print(f"  {task!r}")
    print(f"    → priority: {priority}, category: {category}")
    print()
