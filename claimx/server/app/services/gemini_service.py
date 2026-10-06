import json
from app.core.config import settings

SYSTEM = """You are CLAIMX AI, a neutral insurance FNOL information assistant. Never assign fault, liability, fraud, coverage, approval, settlement, or legal conclusions. Never invent facts. Treat user statements as USER_REPORTED unless independently supported. Use UNKNOWN when information is unavailable and MISSING when required information has not been supplied. Ask only relevant follow-up questions. Keep outputs concise and professional."""

async def ask_gemini(prompt: str, response_schema: dict | None = None) -> str:
    if not settings.gemini_api_key:
        return "Gemini API key is not configured. Please continue with the next relevant accident detail."
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=settings.gemini_api_key)
    config = types.GenerateContentConfig(system_instruction=SYSTEM, temperature=0.2)
    if response_schema:
        config.response_mime_type = "application/json"
        config.response_schema = response_schema
    response = await client.aio.models.generate_content(model="gemini-2.5-flash", contents=prompt, config=config)
    return response.text

async def interview_reply(history: list[dict], latest: str, party: str):
    prompt = f"Party {party} accident interview. Conversation so far: {json.dumps(history[-10:])}. Latest answer: {latest}. Ask the single most useful next question. Do not repeat already answered questions. If the interview has enough core facts, say what is still missing and ask the next highest-value question."
    return await ask_gemini(prompt)

async def extract_statement(text: str, party: str):
    schema = {"type":"OBJECT","properties":{
        "accident_date":{"type":"STRING"},"accident_time":{"type":"STRING"},"location":{"type":"STRING"},"direction_of_travel":{"type":"STRING"},"vehicle":{"type":"STRING"},"other_vehicle":{"type":"STRING"},"speed":{"type":"STRING"},"lane":{"type":"STRING"},"traffic_signal":{"type":"STRING"},"weather":{"type":"STRING"},"road_condition":{"type":"STRING"},"collision_type":{"type":"STRING"},"damage":{"type":"STRING"},"injuries":{"type":"STRING"},"police_involvement":{"type":"STRING"},"tow_requirement":{"type":"STRING"},"witnesses":{"type":"STRING"},"other_details":{"type":"STRING"}
    },"required":[]}
    result = await ask_gemini(f"Extract only explicitly stated facts from this Party {party} statement. Use UNKNOWN for unavailable fields. Statement: {text}", schema)
    try: return json.loads(result)
    except Exception: return {"raw_text": text, "status": "UNSTRUCTURED"}

async def compare_statements(a: dict, b: dict):
    schema={"type":"OBJECT","properties":{"items":{"type":"ARRAY","items":{"type":"OBJECT","properties":{"field":{"type":"STRING"},"party_a":{"type":"STRING"},"party_b":{"type":"STRING"},"status":{"type":"STRING","enum":["AGREED","CONFLICTING","UNKNOWN"]}},"required":["field","party_a","party_b","status"]}}},"required":["items"]}
    result = await ask_gemini(f"Compare these independently collected statements. Do not decide who is truthful. A={json.dumps(a)} B={json.dumps(b)}", schema)
    try: return json.loads(result)
    except Exception: return {"items": []}

async def neutral_summary(accident: dict, statements: list, comparison: dict, missing: list):
    return await ask_gemini(f"Write a neutral 2-4 paragraph FNOL summary. Accident: {json.dumps(accident)} Statements: {json.dumps(statements)} Comparison: {json.dumps(comparison)} Missing: {json.dumps(missing)}. Use 'Party A reported' and 'Party B reported'. Mention conflicts without resolving them. State that unverified information requires human verification.")
