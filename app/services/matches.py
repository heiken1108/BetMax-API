from app.core.external_services import NorskTippingAPI
from app.utils.utils import NT_to_ClubELO_names_mapping
from app.core.schemas import MatchListResponseModel, MatchDetailModel
from app.core.repositories import TeamRatingsRepository, FixturesRepository
from app.core.parsers import MatchParser
from typing import Optional


class MatchesService:
    """Main service for handling match-related operations"""
    def __init__(self):
        self.norsk_tipping_api = NorskTippingAPI()
        self.ratings_repo = TeamRatingsRepository.from_csv(
            'app/files/elo_ratings.csv',
            NT_to_ClubELO_names_mapping
        )
        self.fixtures_repo = FixturesRepository.from_csv('app/files/fixtures.csv', NT_to_ClubELO_names_mapping)
        self.match_parser = MatchParser(self.ratings_repo, self.fixtures_repo)

    async def get_coming_matches(self) -> MatchListResponseModel:
        try:
            data = await self.norsk_tipping_api.get_coming_matches()
            if not data:
                return MatchListResponseModel(eventList=[])
                
            matches = data.get("eventList", [])
            parsed_matches = [
                parsed_match for match in matches
                if (parsed_match := self.match_parser.parse_match(match)) is not None
            ]
            
            return MatchListResponseModel(eventList=parsed_matches)
        except Exception as e:
            print(f"Error getting coming matches: {e}")  # You might want to use proper logging here
            return MatchListResponseModel(eventList=[])
    
    async def get_detailed_match(self, NT_id: str) -> Optional[MatchDetailModel]:
        try:
            data = await self.norsk_tipping_api.get_coming_matches()
            if not data:
                return None
            matches = data.get("eventList", [])
            match = next((m for m in matches if m.get("eventId") == NT_id), None)
            if not match:
                return None
            markets_data = await self.norsk_tipping_api.get_market_for_match(NT_id)
            if not markets_data:
                return None
            markets = markets_data.get("markets", []) 
            
            parsed_match = self.match_parser.parse_detailed_match(match, markets)
            return parsed_match
            
        except Exception as e:
            print(f"Error getting market for match {NT_id}: {e}")
            return None

    async def close(self):
        await self.norsk_tipping_api.close()