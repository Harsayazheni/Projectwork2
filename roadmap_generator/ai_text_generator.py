def generate_ai_text(career, duration, category, item, skill_score):
    """
    Generates AI-style personalized text based on skill gap
    """

    # 🔍 Skill gap interpretation
    if skill_score <= 4:
        gap_level = "weak"
    elif skill_score <= 7:
        gap_level = "medium"
    else:
        gap_level = "strong"

    # 🎯 Templates by category + gap
    templates = {

        "Courses": {
            "weak": f"{item} is highly recommended because this is currently a weak area for you. During the {duration}, you should focus on building strong fundamentals and practicing concepts regularly to close this skill gap for a {career} role.",

            "medium": f"{item} will help you strengthen your existing knowledge and improve consistency. This course bridges the gap between theory and real-world application required in a {career} role.",

            "strong": f"{item} will allow you to refine and optimize your existing expertise. Focus on advanced concepts, edge cases, and real-world implementation scenarios relevant to {career} professionals."
        },

        "Certifications": {
            "weak": f"The {item} certification will help validate your learning and motivate structured preparation in an area where you currently need improvement.",

            "medium": f"Earning the {item} certification will reinforce your skills and improve confidence while applying for {career}-related roles.",

            "strong": f"The {item} certification will act as a credibility booster, showcasing your advanced understanding and commitment to professional growth."
        },

        "Projects": {
            "weak": f"This project is crucial for hands-on learning. It helps convert theoretical understanding into practical skills and significantly reduces gaps in your {career} preparation.",

            "medium": f"Working on {item} will help solidify your understanding and improve problem-solving ability through real-world scenarios.",

            "strong": f"{item} should be treated as a production-level or optimization-focused project to showcase depth and maturity in your {career} skill set."
        },

        "Internships": {
            "weak": f"This internship provides guided exposure where you can learn from experienced professionals and improve weak areas through real-world practice.",

            "medium": f"The {item} allows you to apply your skills in practical environments and become more job-ready for {career} roles.",

            "strong": f"This internship can be used to take ownership of complex tasks, demonstrate leadership, and gain advanced industry exposure."
        }
    }

    # Fallback
    return templates.get(category, {}).get(
        gap_level,
        f"{item} is an important part of your learning journey toward becoming a successful {career}."
    )
