from datetime import datetime, timezone

def next_incident_id(db):
    from app.models.accident import Accident
    year=datetime.now().year
    count=db.query(Accident).count()+1
    return f"CLX-{year}-{count:05d}"
