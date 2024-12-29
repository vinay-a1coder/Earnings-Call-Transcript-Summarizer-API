import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.utils import extract_pdf_text

''' We can't assert the actual summaries, because genai model provides a bit different response on every run'''
class TestEarningsTranscriptSummary(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_valid_input(self):
        """Test with valid input and well-structured transcript."""
        payload = {
            "company_name": "Reliance Industries",
            "transcript_text": "Good morning everyone. Today, we are pleased to report a strong financial performance for the quarter. Our revenue grew by 20% year-on-year, driven by robust demand in the petrochemical and retail segments. We also see significant opportunities in renewable energy. In the coming months, we will expand our footprint in international markets. However, we remain cautious about increasing environmental regulations that could impact our operations. Thank you."
        }
        response = self.client.post("/earnings_transcript_summary", json=payload)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["company_name"], payload["company_name"])
        self.assertIn("financial_performance", data)

    # Test with Sample-Data-1: Earning Call Transcript - Dr Lal Pathlabs.pdf
    def test_with_sample_data_1(self):
        pdf_path = r"C:\Users\Admin\Desktop\Assignments\Earnings-Transcript-Summarizer-API\sample_data\Earning Call Transcript - Dr Lal Pathlabs.pdf"

        pdf_text = extract_pdf_text(pdf_path)
        payload = {
            "company_name": "Dr Lal Pathlabs",
            "transcript_text": pdf_text
        }
        response = self.client.post("/earnings_transcript_summary", json=payload)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["company_name"], payload["company_name"])
        self.assertIn("market_dynamics", data)

    # Test with Sample-Data-2: Earning Call Transcript - One97(Paytm).pdf
    def test_with_sample_data_2(self):
        pdf_path = r"C:\Users\Admin\Desktop\Assignments\Earnings-Transcript-Summarizer-API\sample_data\Earning Call Transcript - One97 (Paytm).pdf"

        pdf_text = extract_pdf_text(pdf_path)
        payload = {
            "company_name": "One 97 Communications Limited",
            "transcript_text": pdf_text
        }
        response = self.client.post("/earnings_transcript_summary", json=payload)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["company_name"], payload["company_name"])
        self.assertIn("expansion_plans", data)
        

    def test_empty_transcript_text(self):
        """Test with an empty transcript_text."""
        payload = {
            "company_name": "Acme Corp",
            "transcript_text": ""
        }
        response = self.client.post("/earnings_transcript_summary", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Transcript text cannot be empty.")

    def test_missing_company_name(self):
        """Test with missing company_name."""
        payload = {
            "transcript_text": "Our financial performance this quarter has been strong."
        }
        response = self.client.post("/earnings_transcript_summary", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_invalid_company_name_type(self):
        """Test with a non-string company_name."""
        payload = {
            "company_name": 12345,
            "transcript_text": "Our revenue growth this quarter was 15%."
        }
        response = self.client.post("/earnings_transcript_summary", json=payload)
        self.assertEqual(response.status_code, 422)

    """Test with irrelevant content in the transcript_text."""
    def test_irrelevant_transcript_1(self):
        payload = {
            "company_name": "Acme Corp",
            "transcript_text": "Revenue growth " * 10000
        }
        response = self.client.post("/earnings_transcript_summary", json=payload)
        output = response.json()
        expected_text_in_response = 'The transcript lacks sufficient meaningful content for analysis. Please provide a detailed transcript.'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_text_in_response, output['detail'])

    def test_irrelevant_transcript_2(self):
        payload = {
            "company_name": "Acme Corp",
            "transcript_text": "The weather has been sunny this week, and we enjoyed a company picnic."
        }
        response = self.client.post("/earnings_transcript_summary", json=payload)
        output = response.json()
        expected_text_in_response = 'The transcript lacks sufficient meaningful content for analysis. Please provide a detailed transcript.'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_text_in_response, output['detail'])

    def test_irrelevant_transcript_3(self):
        """Test with special characters in the transcript."""
        payload = {
            "company_name": "Acme Corp",
            "transcript_text": "Financials: $$$$, Market => Dynamics??? Expansion: Yes/No!"
        }
        response = self.client.post("/earnings_transcript_summary", json=payload)
        output = response.json()
        expected_text_in_response = 'The transcript lacks sufficient meaningful content for analysis. Please provide a detailed transcript.'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_text_in_response, output['detail'])

    def test_no_input_payload(self):
        """Test with no input payload."""
        response = self.client.post("/earnings_transcript_summary", json={})
        self.assertEqual(response.status_code, 422)

    def test_non_english_transcript(self):
        """Test with a non-English transcript."""
        payload = {
            "company_name": "Acme Corp",
            "transcript_text": "Nuestro crecimiento de ingresos fue del 15% este trimestre."
        }
        response = self.client.post("/earnings_transcript_summary", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("financial_performance", data)

if __name__ == "__main__":
    unittest.main()
