from datetime import datetime
from app.services.gemini_service import neutral_summary

def completeness(accident, statements, evidence, policies, missing):
    checks=[bool(accident.claimant_id), bool(accident.vehicle_id), bool(policies), bool(accident.location_text or accident.latitude is not None), bool(accident.accident_time), bool(evidence), any(s.party_label=='A' for s in statements), any(s.party_label=='B' for s in statements)]
    score=round(sum(checks)/len(checks)*100)
    return score

async def build_fnol_data(accident, statements, evidence, missing, policies, profile, vehicle, comparison):
    data={
      "incident_id": accident.incident_id,
      "claimant": profile.full_name if profile else "UNKNOWN",
      "vehicle": f"{vehicle.make} {vehicle.model} ({vehicle.registration_number})" if vehicle else "UNKNOWN",
      "insurance": policies[0].policy_number if policies else "UNKNOWN",
      "accident_time": accident.accident_time.isoformat(),
      "location": accident.location_text or "Location unavailable",
      "gps": f"{accident.latitude}, {accident.longitude}" if accident.latitude is not None and accident.longitude is not None else "UNKNOWN",
      "description": accident.description or "UNKNOWN",
      "party_a": next((s.raw_text for s in statements if s.party_label=='A'), "UNKNOWN"),
      "party_b": next((s.raw_text for s in statements if s.party_label=='B'), "UNKNOWN"),
      "comparison": comparison or {"items":[]},
      "evidence": [{"id":e.evidence_id,"type":e.evidence_type,"file":e.file_name,"status":e.status} for e in evidence],
      "missing": [{"item":m.item,"reason":m.reason} for m in missing],
      "claim_type": accident.claim_type or "UNKNOWN"
    }
    data["readiness"] = completeness(accident, statements, evidence, policies, missing)
    data["summary"] = await neutral_summary(data, [s.structured_data for s in statements], comparison or {}, data["missing"])
    return data
