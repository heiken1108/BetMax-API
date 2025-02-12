from fastapi import APIRouter, HTTPException
from app.services.matches import MatchesService
from datetime import date, datetime, timedelta

router = APIRouter()


@router.get("/")
def health():
	return {"status": "ok"}

@router.get("/matches")
async def get_matches():
	matches_service = MatchesService()
	try:
		matches = await matches_service.get_coming_matches()
		return matches
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		await matches_service.norsk_tipping_api.close()

@router.get("/matches/{NT_id}")
async def get_match(NT_id: str):
	match_service = MatchesService()
	try:
		match = await match_service.get_detailed_match(NT_id)
		if match is None:
			raise HTTPException(status_code=404, detail="Match not found")
		return match
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		await match_service.norsk_tipping_api.close()
