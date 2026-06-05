import unittest

from capstone_checker import check_document


VALID_DOCUMENT = """
Chapter 1
Introduction.
Chapter 2
Methodology.
Chapter 3
Results.
Chapter 4
Abstract.
Chapter 5
Conclusion.
Diagram 1 shows the system architecture.
Figure 1 illustrates the login page.
Table 1 presents evaluation metrics.
References
Smith, J. (2024). Testing Capstones.
Appendix A: Survey Questionnaire.
"""


INVALID_DOCUMENT = """
chapter 1
introduction
This line is duplicated.
This line is duplicated.
As an AI language model, this was generated.
Figure one is shown here.
"""


class TestCapstoneChecker(unittest.TestCase):
    def test_valid_document_passes_all_categories(self):
        result = check_document(VALID_DOCUMENT)
        self.assertTrue(result["overall_passed"])

    def test_invalid_document_reports_expected_failures(self):
        result = check_document(INVALID_DOCUMENT)
        self.assertFalse(result["overall_passed"])
        self.assertFalse(result["grammar"]["passed"])
        self.assertFalse(result["technical_contents"]["passed"])
        self.assertFalse(result["references"]["passed"])
        self.assertFalse(result["ai_contents"]["passed"])

    def test_figure_reference_requires_numeric_label(self):
        result = check_document("Figure one shows interface behavior.")
        self.assertFalse(result["figures"]["passed"])

    def test_grammar_requires_uppercase_sentence_start(self):
        result = check_document("introduction starts lowercase.")
        self.assertFalse(result["grammar"]["passed"])

    def test_similarity_fails_for_heavy_duplicate_lines(self):
        duplicated = "\n".join(["Repeated line."] * 3 + ["Unique one.", "Unique two."])
        result = check_document(duplicated)
        self.assertFalse(result["similarity"]["passed"])


if __name__ == "__main__":
    unittest.main()
