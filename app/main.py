from fastapi import FastAPI, HTTPException
import uvicorn
from app.models import TranscriptInput, TranscriptOutput
from app.ai_service import process_transcript

app = FastAPI()



@app.post("/earnings_transcript_summary", response_model=TranscriptOutput)
async def summarize_transcript(input_data: TranscriptInput):
    if not input_data.transcript_text.strip():
        raise HTTPException(status_code=400, detail="Transcript text cannot be empty.")
    return process_transcript(input_data.company_name, input_data.transcript_text)

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)