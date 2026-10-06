from datetime import datetime, timezone
from app.models.analysis import StatementComparison
from app.services.gemini_service import compare_statements
async def run_comparison(db, accident_id, statements):
    a=next((s.structured_data for s in statements if s.party_label=='A'),{})
    b=next((s.structured_data for s in statements if s.party_label=='B'),{})
    result=await compare_statements(a,b)
    row=StatementComparison(accident_id=accident_id,result=result,created_at=datetime.now(timezone.utc).replace(tzinfo=None)); db.add(row); db.commit(); db.refresh(row); return row
