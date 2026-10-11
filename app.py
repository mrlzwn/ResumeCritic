import pymupdf as fitz  # Modern PyMuPDF import
import streamlit as st
from analyzer import analyze_resume
from report_generator import generate_pdf_report

# Page Configuration
st.set_page_config(
    page_title="ResumeCritic",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


def extract_text_from_pdf(uploaded_file):
  """Extract text from uploaded PDF resume using PyMuPDF."""
  doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
  text = ""
  for page in doc:
    text += page.get_text()
  return text


def main():
  st.title("📄 ResumeCritic")
  st.markdown(
      "AI-Powered Resume Analysis & Professional Diagnostic Scoring Tool"
  )

  # Sidebar for configuration
  st.sidebar.header("Configuration")
  target_role = st.sidebar.selectbox(
      "Target Industry / Role",
      ["Technology / Software", "Finance / Accounting", "General Corporate"],
  )

  # Main uploader
  uploaded_file = st.file_uploader(
      "Upload your Resume (PDF format)", type=["pdf"]
  )

  if uploaded_file is not None:
    with st.spinner("Extracting text and analyzing resume..."):
      resume_text = extract_text_from_pdf(uploaded_file)

      if not resume_text.strip():
        st.error(
            "Could not extract text from this PDF. Please ensure it contains"
            " selectable text."
        )
        return

      # Run analysis
      results = analyze_resume(resume_text, target_role)

    # Display Results Dashboard
    st.success("Analysis Complete!")

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Match Score", f"{results['score']}/100")
    col2.metric("Keyword Density", f"{results['keyword_density']}%")
    col3.metric("Readability Rating", results["readability"])

    st.subheader("Diagnostic Feedback & Suggestions")
    for category, feedback in results["feedback"].items():
      with st.expander(
          f"{category.replace('_', ' ').title()} Recommendations"
      ):
        st.write(feedback)

    # PDF Report Generation
    st.subheader("Download Improvement Report")
    if st.button("Generate PDF Report"):
      pdf_buffer = generate_pdf_report(results, target_role)
      st.download_button(
          label="Download Diagnostic Report",
          data=pdf_buffer,
          file_name="ResumeCritic_Report.pdf",
          mime="application/pdf",
      )


if __name__ == "__main__":
  main()