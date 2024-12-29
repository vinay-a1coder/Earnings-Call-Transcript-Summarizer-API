from pydantic import BaseModel

class TranscriptInput(BaseModel):
    company_name: str
    transcript_text: str

class TranscriptOutput(BaseModel):
    company_name: str
    financial_performance: str
    market_dynamics: str
    expansion_plans: str
    environmental_risks: str
    regulatory_or_policy_changes: str