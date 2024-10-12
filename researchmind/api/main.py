from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from researchmind.researcher.research_assistant import AIResearchAssistant

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


research_assistant = AIResearchAssistant()


class Query(BaseModel):
    query: str


@app.post("/research-project")
async def research_fyp(query: Query):
    response = research_assistant.research(query.query)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("researchmind.api.main:app",
                host="localhost", port=8000, reload=True)
