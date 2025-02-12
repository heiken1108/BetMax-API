from app.core.external_services import NorskTippingAPI
from app.utils.utils import NT_to_ClubELO_names_mapping
from app.core.schemas import MatchListResponseModel
from app.core.repositories import TeamRatingsRepository, FixturesRepository
from app.core.parsers import MatchParser



class MatchesService:
    """Main service for handling match-related operations"""
    def __init__(self):
        self.norsk_tipping_api = NorskTippingAPI()
        self.ratings_repo = TeamRatingsRepository.from_csv(
            'app/files/elo_ratings.csv',
            NT_to_ClubELO_names_mapping
        )
        self.fixtures_repo = FixturesRepository.from_csv('app/files/fixtures.csv')
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

    async def close(self):
        await self.norsk_tipping_api.close()