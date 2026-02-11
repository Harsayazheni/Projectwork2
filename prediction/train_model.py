import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -------------------------------
# 1. Load Dataset
# -------------------------------
data = pd.read_csv("career_data.csv")

# -------------------------------
# 2. Separate Features & Target
# -------------------------------
X = data.drop("Career", axis=1)
y = data["Career"]

# -------------------------------
# 3. Encode Target Labels
# -------------------------------
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# -------------------------------
# 4. Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# -------------------------------
# 5. Train Model
# -------------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X_train, y_train)

# -------------------------------
# 6. Evaluate Model
# -------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# -------------------------------
# 7. Save Model & Encoder
# -------------------------------
with open("career_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("\n✅ Model and Label Encoder saved successfully!")
