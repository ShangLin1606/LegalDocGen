from fastapi import FastAPI, Body
from pydantic import BaseModel
from app.agents.pipeline import LegalDocPipeline, GenerationRequest
from app.utils.pdf import md_to_simple_pdf
from pathlib import Path
import tempfile
app = FastAPI(title="LegalDocGen API")
class GenIn(BaseModel):
    case_title: str
    principal: str
    facts: str
    demands: str
    query: str
    template_name: str = "lawyer_letter.md"
@app.post("/generate")
def generate(data: GenIn):
    pipe = LegalDocPipeline(str(Path(__file__).resolve().parents[2]))
    res = pipe.run(GenerationRequest(**data.model_dump()))
    return res
@app.post("/export_pdf")
def export_pdf(md_text: str = Body(..., embed=True)):
    tmp = Path(tempfile.gettempdir()) / "legal_doc.pdf"
    md_to_simple_pdf(md_text, str(tmp))
    return {"pdf_path": str(tmp)}
