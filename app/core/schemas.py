from pydantic import BaseModel
from datetime import datetime
from typing import List, Union, TypeVar, Generic

class HUBModel(BaseModel):
	home: float
	draw: float
	away: float

class BoolModel(BaseModel):
	true: float
	false: float

T = TypeVar("T", HUBModel, BoolModel)

class MarketModel(BaseModel, Generic[T]):
	name: str
	selections: T
	odds_difference: T
	expected_value: T

class ELOModel(BaseModel):
	home_elo: float
	away_elo: float
	probs: HUBModel
	
class MatchSummaryModel(BaseModel):
	NT_id: str
	home_team: str
	away_team: str
	start_time: datetime
	tournament: str
	odds: HUBModel
	elo: ELOModel
	odds_differences: HUBModel
	expected_value: HUBModel

class MatchDetailModel(BaseModel):
	NT_id: str
	home_team: str
	away_team: str
	start_time: datetime
	tournament: str
	markets: List[MarketModel]
	elo: ELOModel

class MatchListResponseModel(BaseModel):
	eventList: List[MatchSummaryModel]
