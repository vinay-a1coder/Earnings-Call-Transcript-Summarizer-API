import os
from fastapi import HTTPException
import google.generativeai as genai
from app.utils import process_output

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key is not set. Please add it to the .env file.")

genai.configure(api_key=api_key)

def process_transcript(company_name, transcript_text):
    """
    Process the earnings call transcript using the gemini-1.5-flash model to generate summaries
    for the specified categories.

    Args:
        company_name (str): Name of the company.
        transcript_text (str): Earnings call transcript text.

    Returns:
        dict: Summarized response for each category.
    """
    
    categories = [
        "Financial Performance",
        "Market Dynamics",
        "Expansion Plans",
        "Environmental Risks",
        "Regulatory or Policy Changes"
    ]
    
    # Prepare the prompt for the generative model
    prompt = f"""
    Analyze the following earnings call transcript for the company {company_name} and provide a concise summary in these categories:
    1. Financial Performance
    2. Market Dynamics
    3. Expansion Plans
    4. Environmental Risks
    5. Regulatory or Policy Changes

    Transcript:
    {transcript_text}
    """

    try:
        # Generate content using the gemini-1.5-flash model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        summaries = [line.strip() for line in response.text.split("\n") if line.strip()]
        if len(summaries) <= 2 or 'a meaningful analysis is impossible' in response.text.lower():
            raise HTTPException(
                status_code=200, 
                detail="The transcript lacks sufficient meaningful content for analysis. Please provide a detailed transcript."
            )
        
        financial_performance, market_dynamics, expansion_plans, environmental_risks, regulatory_or_policy_changes = process_output(summaries)
        
        output = {
            "company_name": company_name,
            "financial_performance": financial_performance if len(financial_performance) else "N/A",
            "market_dynamics": market_dynamics if len(market_dynamics) else "N/A",
            "expansion_plans": expansion_plans if len(expansion_plans) else "N/A",
            "environmental_risks": environmental_risks if len(environmental_risks) else "N/A",
            "regulatory_or_policy_changes": regulatory_or_policy_changes if len(regulatory_or_policy_changes) else "N/A",
        }
        return output
    except HTTPException:
        raise HTTPException(
                status_code=200, 
                detail="The transcript lacks sufficient meaningful content for analysis. Please provide a detailed transcript."
            )
    except Exception as e:
        raise ValueError(f"Error processing transcript: {str(e)}")
