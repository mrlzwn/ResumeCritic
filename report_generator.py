import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(results, role):
  """Generates a downloadable PDF report summarizing diagnostic feedback."""
  buffer = io.BytesIO()
  doc = SimpleDocTemplate(buffer, pagesize=letter)
  styles = getSampleStyleSheet()
  story = []

  # Title
  story.append(Paragraph("ResumeCritic - Diagnostic Report", styles["Title"]))
  story.append(Spacer(1, 12))

  # Summary Metrics
  story.append(
      Paragraph(f"Target Role: {role}", styles["Heading2"])
  )
  story.append(
      Paragraph(
          f"Overall Match Score: {results['score']}/100", styles["Normal"]
      )
  )
  story.append(
      Paragraph(
          f"Keyword Density: {results['keyword_density']}%", styles["Normal"]
      )
  )
  story.append(
      Paragraph(
          f"Readability Rating: {results['readability']}", styles["Normal"]
      )
  )
  story.append(Spacer(1, 18))

  # Detailed Feedback
  story.append(Paragraph("Diagnostic Recommendations", styles["Heading2"]))
  for category, feedback in results["feedback"].items():
    story.append(
        Paragraph(
            f"<b>{category.replace('_', ' ').title()}:</b> {feedback}",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 8))

  doc.build(story)
  buffer.seek(0)
  return buffer