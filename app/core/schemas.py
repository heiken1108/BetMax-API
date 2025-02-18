from pydantic import BaseModel
from datetime import datetime
from typing import List

class HUBModel(BaseModel):
	home: float
	draw: float
	away: float

class ELORating(BaseModel):
	home_elo: float
	away_elo: float
	probs: HUBModel

class SimpleMatchModel(BaseModel):
	NT_id: str
	home_team: str
	away_team: str
	start_time: datetime
	tournament: str

class MatchModel(SimpleMatchModel):
	odds: HUBModel
	elo: ELORating
	odds_differences: HUBModel
	expected_value: HUBModel

class DetailedMatchModel(MatchModel):
	xGD: float

class MatchListResponseModel(BaseModel):
	eventList: List[MatchModel]

class DetailedMatchResponseModel(BaseModel):
	event: DetailedMatchModel
