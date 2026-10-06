from datetime import datetime, timezone
from app.models.interview import Statement
from app.services.gemini_service import extract_statement
async def save_statement(db, accident_id:int, party_label:str, raw_text:str):
    structured=await extract_statement(raw_text, party_label)
    s=Statement(accident_id=accident_id,party_label=party_label,raw_text=raw_text,structured_data=structured,created_at=datetime.now(timezone.utc).replace(tzinfo=None))
    db.add(s); db.commit(); db.refresh(s); return s
