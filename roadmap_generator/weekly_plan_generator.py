def generate_weekly_plan(career, duration, roadmap, user_scores):
    # Duration → weeks
    if duration == "3":
        total_weeks = 12
    elif duration == "6":
        total_weeks = 24
    else:
        total_weeks = 48

    # Flatten roadmap into ordered focus items
    focus_items = []
    for phase, categories in roadmap.items():
        for category, items in categories.items():
            for item in items:
                focus_items.append((category, item["title"]))

    weekly_plan = []

    # Cycle items across weeks
    for week in range(1, total_weeks + 1):
        index = (week - 1) % len(focus_items)
        category, item = focus_items[index]

        plan_text = generate_week_text(
            career=career,
            category=category,
            item=item,
            user_scores=user_scores,
            week=week,
            total_weeks=total_weeks
        )

        weekly_plan.append({
            "week": week,
            "plan": plan_text
        })

    return weekly_plan
def generate_week_text(career, category, item, user_scores, week, total_weeks):
    avg_skill = sum(user_scores.values()) / len(user_scores)

    if avg_skill <= 4:
        level = "beginner"
    elif avg_skill <= 7:
        level = "intermediate"
    else:
        level = "advanced"

    # Phase awareness
    if week <= total_weeks * 0.3:
        phase = "learning"
    elif week <= total_weeks * 0.7:
        phase = "building"
    else:
        phase = "refining"

    if category == "Courses":
        if phase == "learning":
            return f"Week {week}: Learn the fundamentals of {item}. Focus on understanding core concepts required for a {career}."
        elif phase == "building":
            return f"Week {week}: Apply {item} concepts through exercises and small implementations."
        else:
            return f"Week {week}: Revise advanced topics in {item} and optimize your understanding."

    if category == "Projects":
        if phase == "learning":
            return f"Week {week}: Plan the structure of {item} and understand its requirements."
        elif phase == "building":
            return f"Week {week}: Implement key features of {item} and improve functionality."
        else:
            return f"Week {week}: Refine, debug, and document {item} for portfolio readiness."

    if category == "Certifications":
        return f"Week {week}: Prepare for {item} by revising topics and attempting mock tests."

    if category == "Internships":
        return f"Week {week}: Apply for internships, update resume, and practice interview questions related to {career}."

    return f"Week {week}: Strengthen {item} skills aligned with your {career} roadmap."
def generate_monthly_summaries(career, weekly_plan, user_scores):
    monthly_summaries = []

    total_weeks = len(weekly_plan)
    total_months = max(1, total_weeks // 4)

    avg_skill = sum(user_scores.values()) / len(user_scores)
    base_confidence = avg_skill * 10  # out of 100

    for month in range(1, total_months + 1):
        start = (month - 1) * 4
        end = min(month * 4, total_weeks)

        month_weeks = weekly_plan[start:end]

        # Detect dominant focus
        focus_types = {"Courses": 0, "Projects": 0, "Certifications": 0, "Internships": 0}
        for w in month_weeks:
            for key in focus_types:
                if key.lower() in w["plan"].lower():
                    focus_types[key] += 1

        main_focus = max(focus_types, key=focus_types.get)

        # Phase detection
        if month <= total_months * 0.3:
            phase = "foundation"
            phase_bonus = 0
        elif month <= total_months * 0.7:
            phase = "development"
            phase_bonus = 5
        else:
            phase = "readiness"
            phase_bonus = 10

        progression_bonus = (month / total_months) * 10

        confidence_score = round(
            min(100, base_confidence + phase_bonus + progression_bonus), 1
        )

        summary = (
            f"This month focused mainly on {main_focus.lower()} during the {phase} phase "
            f"of your journey toward becoming a {career}. Your consistency across weeks "
            f"shows measurable improvement and growing confidence."
        )

        monthly_summaries.append({
            "month": month,
            "focus": main_focus,
            "confidence": confidence_score,
            "summary": summary
        })

    return monthly_summaries
def generate_skill_confidence_change(user_scores, duration):
    """
    Generates skill-wise confidence progression
    """

    # Duration multiplier
    if duration == "3":
        growth_factor = 0.25
    elif duration == "6":
        growth_factor = 0.45
    else:
        growth_factor = 0.7

    skill_confidence = {}

    for skill, score in user_scores.items():
        start_confidence = score * 10  # convert to %
        improvement = round((10 - score) * 10 * growth_factor, 1)
        end_confidence = min(100, start_confidence + improvement)

        skill_confidence[skill] = {
            "start": round(start_confidence, 1),
            "end": round(end_confidence, 1),
            "change": round(end_confidence - start_confidence, 1)
        }

    return skill_confidence


