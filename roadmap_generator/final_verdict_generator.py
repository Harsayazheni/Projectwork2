def generate_final_verdict(career, readiness, avg_score, skill_confidence, skills):
    # Determine verdict level
    if readiness >= 80 and avg_score >= 7:
        level = "Job-Ready"
    elif readiness >= 60:
        level = "Near Job-Ready"
    else:
        level = "Foundation Required"

    # Identify strongest & weakest skills
    sorted_skills = sorted(
        skill_confidence.items(),
        key=lambda x: x[1]["end"],
        reverse=True
    )

    strongest = sorted_skills[:2]
    weakest = sorted_skills[-2:]

    strengths = [skills[k] for k, _ in strongest]
    improvements = [skills[k] for k, _ in weakest]

    # Generate verdict text
    verdict = (
        f"You are currently assessed as **{level}** for a career as a {career}. "
        f"Your overall readiness score of {readiness}% and an average skill score "
        f"of {avg_score}/10 indicate solid progress toward industry expectations.\n\n"
        f"### Key Strengths\n"
        f"- {strengths[0]}\n"
        f"- {strengths[1]}\n\n"
        f"### Areas to Improve\n"
        f"- {improvements[0]}\n"
        f"- {improvements[1]}\n\n"
    )

    # Action advice
    if level == "Job-Ready":
        verdict += (
            "### Final Recommendation\n"
            "You should actively apply for roles, internships, or freelance opportunities. "
            "Focus on interview preparation, portfolio polishing, and networking."
        )
    elif level == "Near Job-Ready":
        verdict += (
            "### Final Recommendation\n"
            "You are close to being job-ready. Strengthen the identified weak areas through "
            "hands-on projects and targeted practice before applying aggressively."
        )
    else:
        verdict += (
            "### Final Recommendation\n"
            "You should continue focusing on fundamentals and structured learning. "
            "Once core skills improve, revisit advanced projects and certifications."
        )

    return {
        "level": level,
        "text": verdict
    }
