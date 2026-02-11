from flask import Blueprint, render_template, request
import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Blueprint
resume_bp = Blueprint(
    "resume_bp",
    __name__
)

# ---------------- HELPER FUNCTIONS ---------------- #

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def calculate_similarity(resume_text, job_desc):
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_desc)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([resume_clean, job_clean])

    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0] * 100
    return round(score, 2)

# ---------------- ROUTE ---------------- #

@resume_bp.route("/", methods=["GET", "POST"])
def resume_match():
    score = None
    feedback = None

    if request.method == "POST":
        resume = request.files.get("resume")
        job_desc = request.form.get("job_description")

        if resume and job_desc:
            resume_text = extract_text_from_pdf(resume)
            score = calculate_similarity(resume_text, job_desc)

            if score < 40:
                feedback = "Low Match. Consider tailoring your resume more closely."
            elif score < 70:
                feedback = "Good Match. Your resume aligns fairly well."
            else:
                feedback = "Excellent Match! Your resume strongly aligns."

    return render_template(
        "resume_match.html",
        score=score,
        feedback=feedback
    )
