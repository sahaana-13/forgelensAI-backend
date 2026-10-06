import os, uuid
from datetime import datetime, timezone
from fastapi import UploadFile, HTTPException
from app.core.config import settings
ALLOWED={"image/jpeg","image/png","application/pdf"}
async def save_upload(file: UploadFile):
    if file.content_type not in ALLOWED: raise HTTPException(400,"Only JPG, JPEG, PNG and PDF are allowed")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024: raise HTTPException(400,"File exceeds size limit")
    os.makedirs(settings.upload_dir,exist_ok=True)
    ext=os.path.splitext(file.filename or "file")[1].lower()
    name=f"{uuid.uuid4().hex}{ext}"; path=os.path.join(settings.upload_dir,name)
    with open(path,"wb") as f: f.write(data)
    return name,path
