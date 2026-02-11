from flask import Blueprint, render_template, request, send_file
import json

from .roadmap_data import career_roadmaps, career_skills
from .pdf_generator import generate_pdf
from .ai_text_generator import generate_ai_text
from .weekly_plan_generator import (
    generate_weekly_plan,
    generate_monthly_summaries,
    generate_skill_confidence_change
)
from .final_verdict_generator import generate_final_verdict


# ===============================
# 🔷 Blueprint Definition
# ===============================
roadmap_bp = Blueprint(
    "roadmap",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/roadmap"
)


# ===============================
# 🏠 Roadmap Home Page
# ===============================
@roadmap_bp.route("/")
def index():
    return render_template(
        "index.html",
        careers=career_skills.keys(),
        career_skills=json.dumps(career_skills)
    )


# ===============================
# ⚙️ Generate Roadmap
# ===============================
@roadmap_bp.route("/generate", methods=["POST"])
def generate():
    career = request.form["career"]
    skills = career_skills[career]

    # ===============================
    # 1️⃣ Calculate Skill Scores
    # ===============================
    total_score = 0
    user_scores = {}

    for key in skills:
        score = int(request.form.get(f"skill_{key}", 5))
        user_scores[key] = score
        total_score += score

    avg_score = round(total_score / len(skills), 2)

    # ===============================
    # 🔥 Category → Skill Mapping
    # ===============================
    category_skill_map = {
        "Courses": list(skills.keys())[0],
        "Certifications": list(skills.keys())[1],
        "Projects": list(skills.keys())[2],
        "Internships": list(skills.keys())[3]
    }

    # ===============================
    # 2️⃣ Career Readiness
    # ===============================
    readiness = total_score  # max = 100

    if readiness >= 80:
        readiness_level = "Job-Ready"
    elif readiness >= 60:
        readiness_level = "Intermediate"
    else:
        readiness_level = "Beginner"

    # ===============================
    # 3️⃣ Duration Decision Logic
    # ===============================
    if avg_score >= 7.5:
        duration = "3"
        selected_roadmap = {
            "3 Months": career_roadmaps[career]["short_term"]
        }
    elif avg_score >= 5.0:
        duration = "6"
        selected_roadmap = {
            "6 Months": career_roadmaps[career]["mid_term"]
        }
    else:
        duration = "12"
        selected_roadmap = {
            "3 Months": career_roadmaps[career]["short_term"],
            "6 Months": career_roadmaps[career]["mid_term"]
        }

    # ===============================
    # 4️⃣ AI-STYLE TEXT (SKILL-GAP AWARE)
    # ===============================
    ai_roadmap = {}

    for phase, categories in selected_roadmap.items():
        ai_roadmap[phase] = {}

        for category, items in categories.items():
            ai_roadmap[phase][category] = []

            for item in items:
                skill_score = user_scores.get(
                    category_skill_map.get(category),
                    avg_score
                )

                ai_roadmap[phase][category].append({
                    "title": item,
                    "description": generate_ai_text(
                        career=career,
                        duration=phase,
                        category=category,
                        item=item,
                        skill_score=skill_score
                    )
                })

    # ===============================
    # 5️⃣ Weekly AI Plan
    # ===============================
    weekly_plan = generate_weekly_plan(
        career=career,
        duration=duration,
        roadmap=ai_roadmap,
        user_scores=user_scores
    )

    # ===============================
    # 6️⃣ Monthly AI Summaries
    # ===============================
    monthly_summaries = generate_monthly_summaries(
        career=career,
        weekly_plan=weekly_plan,
        user_scores=user_scores
    )

    # ===============================
    # 7️⃣ Skill-wise Confidence Change
    # ===============================
    skill_confidence = generate_skill_confidence_change(
        user_scores=user_scores,
        duration=duration
    )

    # ===============================
    # 8️⃣ Final AI Career Verdict
    # ===============================
    final_verdict = generate_final_verdict(
        career=career,
        readiness=readiness,
        avg_score=avg_score,
        skill_confidence=skill_confidence,
        skills=skills
    )

    # ===============================
    # 9️⃣ Render Result Page
    # ===============================
    return render_template(
        "result.html",
        career=career,
        duration=duration,
        roadmap=ai_roadmap,
        avg_score=avg_score,
        readiness=readiness,
        readiness_level=readiness_level,
        skills=skills,
        user_scores=user_scores,
        weekly_plan=weekly_plan,
        monthly_summaries=monthly_summaries,
        skill_confidence=skill_confidence,
        final_verdict=final_verdict
    )


# ===============================
# 📄 Download PDF
# ===============================
@roadmap_bp.route("/download", methods=["POST"])
def download():
    career = request.form["career"]
    duration = request.form["duration"]
    avg_score = float(request.form["avg_score"])

    skills = career_skills[career]

    user_scores = {
        key: int(request.form.get(f"skill_{key}", 5))
        for key in skills
    }

    readiness = sum(user_scores.values())

    # 🔥 SAME category → skill mapping
    category_skill_map = {
        "Courses": list(skills.keys())[0],
        "Certifications": list(skills.keys())[1],
        "Projects": list(skills.keys())[2],
        "Internships": list(skills.keys())[3]
    }

    # 🔥 Select roadmap
    if duration == "3":
        selected_roadmap = {
            "3 Months": career_roadmaps[career]["short_term"]
        }
    elif duration == "6":
        selected_roadmap = {
            "6 Months": career_roadmaps[career]["mid_term"]
        }
    else:
        selected_roadmap = {
            "3 Months": career_roadmaps[career]["short_term"],
            "6 Months": career_roadmaps[career]["mid_term"]
        }

    # 🔥 BUILD AI ROADMAP AGAIN (THIS WAS MISSING)
    ai_roadmap = {}

    for phase, categories in selected_roadmap.items():
        ai_roadmap[phase] = {}

        for category, items in categories.items():
            ai_roadmap[phase][category] = []

            for item in items:
                skill_score = user_scores.get(
                    category_skill_map.get(category),
                    avg_score
                )

                ai_roadmap[phase][category].append({
                    "title": item,
                    "description": generate_ai_text(
                        career=career,
                        duration=phase,
                        category=category,
                        item=item,
                        skill_score=skill_score
                    )
                })

    # 🔥 Final verdict
    skill_confidence = generate_skill_confidence_change(
        user_scores=user_scores,
        duration=duration
    )

    final_verdict = generate_final_verdict(
        career=career,
        readiness=readiness,
        avg_score=avg_score,
        skill_confidence=skill_confidence,
        skills=skills
    )

    pdf = generate_pdf(
        career,
        avg_score,
        duration,
        skills,
        user_scores,
        ai_roadmap,          # ✅ FIXED
        final_verdict
    )

    return send_file(pdf, as_attachment=True)

