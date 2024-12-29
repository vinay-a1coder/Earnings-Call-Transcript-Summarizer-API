# Earnings Call Transcript Summarizer API

This project provides a RESTful API built with FastAPI to summarize earnings call transcripts for companies. The API categorizes the summary into specific sections such as financial performance, market dynamics, expansion plans, environmental risks, and regulatory or policy changes, using a Generative AI model (`gemini-1.5-flash`).

---

## Features
- Accepts an earnings call transcript and generates a categorized summary.
- Uses the `gemini-1.5-flash` Generative AI model for text processing.
- Dockerized for easy deployment.

---

## Installation and Setup

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- GEMINI API Key for accessing the Generative AI model

---

### Local Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vinay-a1coder/Earnings-Call-Transcript-Summarizer-API.git
   cd Earnings-Transcript-Summarizer-API

2. **Create and Activate a Virtual Environment (Optional):**
    ```bash
    python -m venv venv
    source venv/bin/activate   # For Linux/Mac
    venv\Scripts\activate      # For Windows

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Run the Application:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000


---

### Docker Setup

1. **Set the Environment Variable:**

    In Linux/WSL:
    ```bash
    export GEMINI_API_KEY="your_actual_gemini_api_key"

    In PowerShell:
    ```powershell
    $env:GEMINI_API_KEY="your_actual_gemini_api_key"

2. **Build and Run the Docker Container:**

    ```bash
    docker-compose build
    docker-compose up

3. **Access the API Using Postman or cURL:**

    1. **Use Postman to send requests to the API endpoint:**

        ```bash
        POST http://0.0.0.0:8000/earnings_transcript_summary

        Example request body:

        ```json
        {
            "company_name": "Acme Corp",
            "transcript_text": "Full earnings call transcript goes here..."
        }
    
    2. **Alternatively, you can use curl:**

        ```bash
        curl -X POST "http://localhost:8000/earnings_transcript_summary" \
        -H "Content-Type: application/json" \
        -d '{"company_name": "Acme Corp", "transcript_text": "Full earnings call transcript goes here..."}'


4. **Stop the Container:**

    ```bash
    docker-compose down

---

### API Endpoints
1. **Summarize Earnings Call Transcript**

    URL: /earnings_transcript_summary
    Method: POST
    Request Body:

    ```json
    {
    "company_name": "Acme Corp",
    "transcript_text": "Full earnings call transcript goes here..."
    }

    Response:
    ```json
    {
    "company_name": "Acme Corp",
    "financial_performance": "Summary of financial performance.",
    "market_dynamics": "Summary of market dynamics.",
    "expansion_plans": "Summary of expansion plans.",
    "environmental_risks": "Summary of environmental risks.",
    "regulatory_or_policy_changes": "Summary of regulatory or policy changes."
    }

---

### Running Tests

1. **Run Tests with pytest:**

    ```bash
    python -m pytest tests\test_transcript_summary.py

---

### Project Structure

    ```bash
    EARNINGS-TRANSCRIPT-SUMMARIZER-API/
    ├── app/
    │   ├── __init__.py                                         # Marks this directory as a Python package.
    │   ├── ai_service.py                                       # Model to process transcript
    │   ├── main.py                                             # FastAPI application
    │   ├── models.py                                           # Data models
    │   └── utils.py                                            # Helper functions
    ├── sample_data/                                            # Sample data for testing
    │   ├── Earning Call Transcript - Dr Lal Pathlabs.pdf
    │   ├── Earning Call Transcript - One97(Paytm).pdf
    ├── tests/                      
    │   ├── test_transcript_summary.py                          # Testcases
    ├── Dockerfile                                              # Docker configuration
    ├── docker-compose.yml                                      # Docker Compose configuration
    ├── requirements.txt                                        # Python dependencies
    ├── .env                                                    # Environment Variables
    └── README.md                                               # Project documentation
