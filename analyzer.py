import re


def analyze_resume(text, role):
  """Analyzes resume text against targeted industry keywords and metrics."""
  keywords = {
      "Technology / Software": [
          "python",
          "sql",
          "git",
          "api",
          "cloud",
          "agile",
          "ci/cd",
          "docker",
      ],
      "Finance / Accounting": [
          "excel",
          "financial modeling",
          "forecasting",
          "audit",
          "gaap",
          "budgeting",
      ],
      "General Corporate": [
          "project management",
          "leadership",
          "strategy",
          "communication",
          "stakeholders",
      ],
  }

  target_keywords = keywords.get(role, keywords["General Corporate"])
  found_keywords = [
      kw for kw in target_keywords if re.search(r"\b" + kw + r"\b", text.lower())
  ]

  # Simple metric calculation
  score = int((len(found_keywords) / len(target_keywords)) * 100)
  words = text.split()
  keyword_density = round((len(found_keywords) / max(len(words), 1)) * 100, 2)

  readability = "High" if len(words) > 150 else "Medium"

  feedback = {
      "keyword_optimization": (
          f"Found {len(found_keywords)} of {len(target_keywords)} key skills:"
          f" {', '.join(found_keywords) if found_keywords else 'None'}."
      ),
      "formatting_&_length": (
          f"Total word count is {len(words)}. Ensure your bullet points are"
          " concise and action-oriented."
      ),
      "action_verbs": (
          "Consider starting bullet points with strong action verbs like"
          " 'Engineered', 'Optimized', or 'Managed'."
      ),
  }

  return {
      "score": score,
      "keyword_density": keyword_density,
      "readability": readability,
      "feedback": feedback,
  }