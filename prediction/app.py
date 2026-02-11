"""
Prediction Module - Career Prediction and Skill Analysis
"""

from flask import Blueprint, render_template, request, session
import pickle
import numpy as np

# Create Blueprint for prediction module
prediction_bp = Blueprint(
    'prediction',
    __name__,
    template_folder='templates',
    static_folder='static'
)


# Load trained model
model = pickle.load(open("prediction/career_model.pkl", "rb"))
label_encoder = pickle.load(open("prediction/label_encoder.pkl", "rb"))

career_info = {
    "Software Developer": "Builds, tests, and maintains software applications.",
    "Data Scientist": "Analyzes complex data to extract insights.",
    "AI ML Engineer": "Designs intelligent systems using machine learning.",
    "UI/UX Designer": "Creates intuitive and user-friendly interfaces.",
    "Project Manager": "Plans, executes, and manages projects effectively.",
    "Business Analyst": "Analyzes business needs and requirements."
}

ideal_skills = {
    "Software Developer": {
        "Programming_Skill":9,"Logical_Thinking":8,"Math_Statistics":6,
        "Analytical_Skills":7,"Problem_Solving":9,"Creativity":5,
        "Interest_Design":4,"Communication":6,"Leadership":5,
        "Teamwork":7,"Adaptability":7,"Time_Management":7,
        "Interest_AI":6,"Industry_Awareness":6,"CGPA":7
    },
    "Data Scientist": {
        "Programming_Skill":7,"Logical_Thinking":9,"Math_Statistics":9,
        "Analytical_Skills":9,"Problem_Solving":8,"Creativity":5,
        "Interest_Design":3,"Communication":6,"Leadership":5,
        "Teamwork":6,"Adaptability":7,"Time_Management":7,
        "Interest_AI":9,"Industry_Awareness":7,"CGPA":8
    },
    "AI ML Engineer": {
        "Programming_Skill":9,"Logical_Thinking":9,"Math_Statistics":9,
        "Analytical_Skills":9,"Problem_Solving":9,"Creativity":5,
        "Interest_Design":3,"Communication":6,"Leadership":5,
        "Teamwork":6,"Adaptability":7,"Time_Management":7,
        "Interest_AI":10,"Industry_Awareness":7,"CGPA":8
    },
    "UI/UX Designer": {
        "Programming_Skill":4,"Logical_Thinking":5,"Math_Statistics":3,
        "Analytical_Skills":5,"Problem_Solving":6,"Creativity":9,
        "Interest_Design":9,"Communication":8,"Leadership":5,
        "Teamwork":7,"Adaptability":8,"Time_Management":7,
        "Interest_AI":3,"Industry_Awareness":6,"CGPA":6
    }
}

@prediction_bp.route("/")
def index():
    """Home page with prediction form"""
    return render_template("home.html")

@prediction_bp.route("/prediction", methods=["GET", "POST"])
def prediction():
    """Handle career prediction"""
    if request.method == "POST":
        features = [
            "Programming_Skill","Logical_Thinking","Math_Statistics",
            "Analytical_Skills","Problem_Solving","Creativity",
            "Interest_Design","Communication","Leadership","Teamwork",
            "Adaptability","Time_Management","Interest_AI",
            "Industry_Awareness","CGPA"
        ]

        values = [float(request.form[f]) for f in features]
        X = np.array(values).reshape(1, -1)

        pred_label = model.predict(X)[0]
        pred_career = label_encoder.inverse_transform([pred_label])[0]

        # Store in session for other modules to access
        session.clear()
        session["prediction"] = pred_career
        session["skills"] = dict(zip(features, values))
        session["ideal"] = ideal_skills.get(pred_career, session["skills"])
        session["description"] = career_info.get(
            pred_career,
            "Career description not available."
        )

    return render_template(
        "prediction.html",
        prediction=session.get("prediction"),
        description=session.get("description")
    )

@prediction_bp.route("/visualization")
def visualization():
    """Display skill visualization"""
    if "skills" not in session or "ideal" not in session:
        return render_template("visualization.html", error=True)

    return render_template(
        "visualization.html",
        skills=session["skills"],
        ideal=session["ideal"],
        prediction=session.get("prediction"),
        error=False
    )