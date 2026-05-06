import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.case import Judgment
from app.schemas.judgment import JudgmentUploadResponse, JudgmentStatus, JudgmentDetail
from app.core.security import get_current_user
from app.workers.processor import process_judgment_task

router = APIRouter(prefix="/judgments", tags=["Judgments"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=JudgmentUploadResponse)
async def upload_judgment(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files accepted")

    judgment_id = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_DIR, f"{judgment_id}.pdf")

    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    judgment = Judgment(
        id=judgment_id,
        pdf_path=pdf_path,
        pdf_filename=file.filename,
        processing_status="pending",
        progress=0
    )
    db.add(judgment)
    db.commit()

    background_tasks.add_task(process_judgment_task, judgment_id, pdf_path)

    return JudgmentUploadResponse(
        judgment_id=judgment_id,
        status="processing",
        message="PDF uploaded. Processing started."
    )

@router.get("/{judgment_id}/status", response_model=JudgmentStatus)
def get_status(judgment_id: str, db: Session = Depends(get_db)):
    j = db.query(Judgment).filter(Judgment.id == judgment_id).first()
    if not j:
        raise HTTPException(404, "Judgment not found")
    return JudgmentStatus(
        judgment_id=judgment_id,
        status=j.processing_status,
        progress=j.progress or 0,
        message=j.error_message
    )

@router.get("/{judgment_id}", response_model=JudgmentDetail)
def get_judgment(judgment_id: str, db: Session = Depends(get_db)):
    j = db.query(Judgment).filter(Judgment.id == judgment_id).first()
    if not j:
        raise HTTPException(404, "Judgment not found")
    return {
        "id": j.id,
        "case_number": j.case_number,
        "order_date": j.order_date,
        "pdf_filename": j.pdf_filename,
        "pdf_url": f"/judgments/{j.id}/file",
        "processing_status": j.processing_status,
        "total_pages": j.total_pages,
        "has_kannada": j.has_kannada,
        "action_items": j.action_items,
        "appeal_windows": j.appeal_windows,
    }

@router.get("/{judgment_id}/file")
def get_judgment_file(judgment_id: str, db: Session = Depends(get_db)):
    j = db.query(Judgment).filter(Judgment.id == judgment_id).first()
    if not j:
        raise HTTPException(404, "Judgment not found")

    pdf_path = _resolve_pdf_path(j)
    if not pdf_path:
        raise HTTPException(404, "PDF file not found")

    return FileResponse(pdf_path, media_type="application/pdf", filename=j.pdf_filename or pdf_path.name)

@router.get("/")
def list_judgments(db: Session = Depends(get_db)):
    judgments = db.query(Judgment).order_by(Judgment.created_at.desc()).limit(20).all()
    return [{"id": j.id, "filename": j.pdf_filename, "status": j.processing_status, 
             "case_number": j.case_number, "created_at": str(j.created_at)} for j in judgments]

def _resolve_pdf_path(judgment: Judgment) -> Path | None:
    candidates = []
    if judgment.pdf_path:
        candidates.append(Path(judgment.pdf_path))
    if judgment.pdf_filename:
        candidates.append(Path(UPLOAD_DIR) / judgment.pdf_filename)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None
