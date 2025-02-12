from pydantic import BaseModel
from datetime import datetime
from typing import List

class Odds(BaseModel):
	home: float
	draw: float
	away: float

class ELOProbs(BaseModel):
	home_prob: float
	draw_prob: float
	away_prob: float

class ELORating(BaseModel):
	home_elo: float
	away_elo: float
	probs: ELOProbs

class SimpleMatchModel(BaseModel):
	NT_id: str
	home_team: str
	away_team: str
	start_time: datetime
	tournament: str

class MatchModel(SimpleMatchModel):
	odds: Odds
	elo: ELORating

class DetailedMatchModel(MatchModel):
	xGD: float

class MatchListResponseModel(BaseModel):
	eventList: List[MatchModel]

class DetailedMatchResponseModel(BaseModel):
	event: DetailedMatchModel
