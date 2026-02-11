from flask import Blueprint, render_template, request
import pickle
import re
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

fakejob_bp = Blueprint(
    "fakejob",
    __name__,
    url_prefix="/fakejob",
    template_folder="templates",
    static_folder="static"
)

# Load model
model = pickle.load(open(os.path.join(BASE_DIR, "model/model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "model/vectorizer.pkl"), "rb"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

SCAM_KEYWORDS = [
    "daily payout", "no experience", "work from home",
    "guaranteed income", "easy money", "high pay"
]

def scam_keyword_boost(text, prob):
    count = sum(1 for k in SCAM_KEYWORDS if k in text)
    return min(prob + count * 0.07, 1.0)

@fakejob_bp.route("/")
def index():
    # looks for templates/fakejob/index.html
    return render_template("fakejob/index.html")

@fakejob_bp.route("/predict", methods=["POST"])
def predict():
    fields = [
        request.form.get("title", ""),
        request.form.get("description", ""),
        request.form.get("company_profile", ""),
        request.form.get("requirements", ""),
        request.form.get("benefits", ""),
        request.form.get("location", "")
    ]

    text = clean_text(" ".join(fields))
    vec = vectorizer.transform([text])

    prob = model.predict_proba(vec)[0][1]
    prob = scam_keyword_boost(text, prob)

    label = "Fake Job 🚨" if prob > 0.3 else "Real Job ✅"
    risk = (
        "High Risk" if prob >= 0.6
        else "Medium Risk" if prob >= 0.3
        else "Low Risk"
    )

    return render_template(
        "fakejob/result.html",
        prediction=label,
        probability=round(prob, 2),
        risk=risk
    )

@fakejob_bp.route("/bulk", methods=["POST"])
def bulk():
    file = request.files["csv_file"]
    df = pd.read_csv(file)

    cols = ['title', 'description', 'company_profile', 'requirements', 'benefits', 'location']
    df['text'] = df[cols].fillna("").agg(' '.join, axis=1)
    df['text'] = df['text'].apply(clean_text)

    vecs = vectorizer.transform(df['text'])
    probs = model.predict_proba(vecs)[:, 1]

    df['Prediction'] = ["Fake Job 🚨" if p > 0.3 else "Real Job ✅" for p in probs]
    df['Probability'] = [round(p, 2) for p in probs]

    table_html = df[['title', 'Prediction', 'Probability']].to_html(
        classes="table",
        index=False
    )

    return render_template("fakejob/bulk_result.html", table=table_html)
