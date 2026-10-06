from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth, profile, vehicles, insurance, accidents, evidence, interviews, ai, statements, analysis, fnol, notifications, admin
from app import models
Base.metadata.create_all(bind=engine)
os.makedirs(settings.upload_dir,exist_ok=True)
app=FastAPI(title="CLAIMX API",version="1.0.0",description="AI-powered digital accident reporting and FNOL platform")
app.add_middleware(CORSMiddleware,allow_origins=[settings.frontend_url],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/uploads",StaticFiles(directory=settings.upload_dir),name="uploads")
for r in [auth.router,profile.router,vehicles.router,insurance.router,accidents.router,evidence.router,interviews.router,ai.router,statements.router,analysis.router,fnol.router,notifications.router,admin.router]: app.include_router(r)
@app.get("/")
def root(): return {"name":"CLAIMX","message":"From Accident to Evidence-Ready Claim.","docs":"/docs"}
@app.get("/health")
def health(): return {"status":"ok"}
