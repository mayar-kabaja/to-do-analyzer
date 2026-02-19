import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

_script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(_script_dir, "data", "cleaned_tasks.csv"))

X = df["text"]
y_priority = df["priority"]
y_category = df["category"]

X_train, X_test, yp_train, yp_test, yc_train, yc_test = train_test_split(
    X, y_priority, y_category, test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

priority_model = LogisticRegression()
priority_model.fit(X_train_vec, yp_train)

category_model = LogisticRegression()
category_model.fit(X_train_vec, yc_train)

_models_dir = os.path.join(_script_dir, "models")
os.makedirs(_models_dir, exist_ok=True)

with open(os.path.join(_models_dir, "priority_model.pkl"), 'wb') as f:
    pickle.dump(priority_model, f)

with open(os.path.join(_models_dir, "category_model.pkl"), 'wb') as f:
    pickle.dump(category_model, f)

with open(os.path.join(_models_dir, "vectorizer.pkl"), 'wb') as f:
    pickle.dump(vectorizer, f)

print("Models saved to models/")