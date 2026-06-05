from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

from .database import get_connection


def wrap_text(text, max_width=80):
    if not text:
        return []
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        if len(' '.join(current_line + [word])) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines


def generate_report_pdf(user_id: int) -> bytes:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, full_name, email, age, gender, created_at
        FROM users
        WHERE id = %s
    """, (user_id,))
    user = cursor.fetchone()

    cursor.execute("""
        SELECT id, symptoms, risk_level, risk_score, ai_summary, created_at
        FROM symptom_history
        WHERE user_id = %s
        ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()

    conn.close()

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    left_margin = 50
    right_margin = width - 50

    y = height - 50

    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(left_margin, y, "HealthGuard - Patient Health Report")
    y -= 30

    # Generated date
    p.setFont("Helvetica", 9)
    gen_date = datetime.utcnow().strftime("%B %d, %Y at %H:%M UTC")
    p.drawString(left_margin, y, f"Generated: {gen_date}")
    y -= 20

    # Patient info
    if user:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(left_margin, y, "Patient Information")
        y -= 16

        p.setFont("Helvetica", 10)
        p.drawString(left_margin, y, f"Name: {user[1]}")
        y -= 14
        p.drawString(left_margin, y, f"Patient ID: {user[0]}")
        y -= 14
        p.drawString(left_margin, y, f"Email: {user[2]}")
        y -= 14
        p.drawString(left_margin, y, f"Age: {user[3]}, Gender: {user[4] or 'Not specified'}")
        y -= 20

    # Health sessions
    p.setFont("Helvetica-Bold", 12)
    p.drawString(left_margin, y, "Recent Health Sessions")
    y -= 18

    session_num = 0
    for row in rows[:10]:
        if y < 100:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 10)

        session_num += 1
        p.setFont("Helvetica-Bold", 10)
        p.drawString(left_margin, y, f"Session {session_num}")
        y -= 12

        p.setFont("Helvetica", 9)
        p.drawString(left_margin, y, f"Date: {row[5]}")
        y -= 11
        p.drawString(left_margin, y, f"Risk Level: {row[2]} (Score: {row[3]})")
        y -= 12

        # Symptoms
        symptoms = row[1] or 'No symptoms recorded'
        p.setFont("Helvetica-Bold", 9)
        p.drawString(left_margin, y, "Symptoms:")
        y -= 11
        p.setFont("Helvetica", 9)
        symptom_lines = wrap_text(symptoms, 60)
        for line in symptom_lines[:3]:
            p.drawString(left_margin + 20, y, line)
            y -= 10

        # Summary
        summary = (row[4] or 'No summary available').strip()
        p.setFont("Helvetica-Bold", 9)
        p.drawString(left_margin, y, "AI Summary:")
        y -= 11
        p.setFont("Helvetica", 9)
        summary_lines = wrap_text(summary, 70)
        for line in summary_lines[:5]:
            p.drawString(left_margin + 20, y, line)
            y -= 10

        y -= 8

    # Footer
    if y < 80:
        p.showPage()
        y = height - 50

    p.setFont("Helvetica-Oblique", 8)
    footer_text = "This report is for informational purposes only. Not a substitute for professional medical advice."
    p.drawString(left_margin, 30, footer_text)

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer.read()