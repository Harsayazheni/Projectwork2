from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def generate_pdf(
    career,
    avg_score,
    duration,
    skills,
    user_scores,
    roadmap,
    final_verdict
):
    filename = f"{career}_AI_Career_Roadmap.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    margin_x = 50
    y = height - 50

    def new_page():
        nonlocal y
        c.showPage()
        y = height - 50
        c.setFont("Helvetica", 10)

    # ===============================
    # PAGE 1: OVERVIEW
    # ===============================
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin_x, y, f"{career} – AI Career Roadmap")
    y -= 35

    c.setFont("Helvetica", 11)
    c.drawString(margin_x, y, f"Average Skill Score: {avg_score} / 10")
    y -= 18
    c.drawString(margin_x, y, f"Recommended Duration: {duration} Months")
    y -= 30

    # ===============================
    # SKILL OVERVIEW
    # ===============================
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_x, y, "Skill Overview")
    y -= 20

    c.setFont("Helvetica", 10)
    for key, label in skills.items():
        c.drawString(margin_x + 10, y, f"{label}: {user_scores[key]}/10")
        y -= 14
        if y < 80:
            new_page()

    # ===============================
    # ROADMAP PAGES
    # ===============================
    for phase, categories in roadmap.items():
        new_page()

        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin_x, y, phase)
        y -= 30

        for category, items in categories.items():
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin_x + 10, y, category)
            y -= 18

            c.setFont("Helvetica", 10)
            for item in items:
                # Title
                c.drawString(margin_x + 25, y, f"• {item['title']}")
                y -= 14

                # Description (wrap manually)
                text = c.beginText(margin_x + 40, y)
                text.setLeading(14)

                for line in item["description"].split(". "):
                    text.textLine(line.strip())

                c.drawText(text)
                y = text.getY() - 10

                if y < 100:
                    new_page()

    # ===============================
    # FINAL PAGE: AI VERDICT
    # ===============================
    new_page()

    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin_x, y, "Final AI Career Verdict")
    y -= 35

    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin_x, y, f"Verdict Level: {final_verdict['level']}")
    y -= 25

    c.setFont("Helvetica", 11)
    verdict_text = final_verdict["text"].split("\n")

    for line in verdict_text:
        c.drawString(margin_x, y, line)
        y -= 16
        if y < 80:
            new_page()

    c.save()
    return filename
