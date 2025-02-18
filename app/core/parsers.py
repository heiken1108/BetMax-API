from datetime import datetime
from typing import Dict, Optional
from .schemas import MatchModel, Odds, ELORating, DetailedMatchModel, HUBDifferences
from .repositories import TeamRatingsRepository, FixturesRepository
from app.utils.utils import tournaments_of_interest

class MatchParser:
    """Handles parsing of raw match data into MatchModel objects"""
    def __init__(self, ratings_repo: TeamRatingsRepository, fixtures_repo: FixturesRepository):
        self.ratings_repo = ratings_repo
        self.fixtures_repo = fixtures_repo

    def is_valid_match(self, match: Dict) -> bool:
        if not match:
            return False
            
        tournament = match.get("tournament", {})
        main_market = match.get('mainMarket', {})
        selections = main_market.get('selections', [])
        
        return all([
            tournament,
            tournament.get("name") in tournaments_of_interest,
            match.get("homeParticipant"),
            match.get("awayParticipant"),
            main_market,
            len(selections) >= 3,
            main_market.get('marketName') == 'HUB'
        ])

    def parse_odds(self, market_data: Dict) -> Optional[Odds]:
        if not market_data:
            return None
            
        selections = market_data.get('selections', [])
        if len(selections) < 3:
            return None
            
        try:
            return Odds(
                home=selections[0].get('selectionOdds', 0),
                draw=selections[1].get('selectionOdds', 0),
                away=selections[2].get('selectionOdds', 0)
            )
        except (IndexError, TypeError):
            return None

    def parse_match(self, match: Dict) -> Optional[MatchModel]:
        if not self.is_valid_match(match):
            return None

        try:
            home_team = match.get("homeParticipant", '')
            away_team = match.get("awayParticipant", '')
            odds = self.parse_odds(match.get('mainMarket', {}))
            probs = self.fixtures_repo.get_match_probabilities(
                        home_team, 
                        away_team, 
                        self.ratings_repo.name_mapping
                    )
            
            if not odds:
                return None

            return MatchModel(
                NT_id=match.get("eventId", ''),
                home_team=home_team,
                away_team=away_team,
                start_time=datetime.fromisoformat(match.get("startTime", '')),
                tournament=match.get("tournament", {}).get("name", ''),
                odds=odds,
                elo=ELORating(
                    home_elo=self.ratings_repo.get_elo_rating(home_team),
                    away_elo=self.ratings_repo.get_elo_rating(away_team),
                    probs=probs
                ),
                odds_differences=HUBDifferences(
                    home=odds.home - (1/probs.home_prob) if probs.home_prob > 0 else 0,
                    draw=odds.draw - (1/probs.draw_prob) if probs.draw_prob > 0 else 0,
                    away=odds.away - (1/probs.away_prob) if probs.away_prob > 0 else 0
                )
            )
        except (ValueError, TypeError, KeyError) as e:
            print(f"Error parsing match: {e}")  # You might want to use proper logging here
            return None
    
    def parse_detailed_match(self, match: Dict) -> Optional[DetailedMatchModel]:
        match_model = self.parse_match(match)
        if not match_model:
            return None
        xGD = 1.0 #Egentlig match.home_team og match.away_team
        return DetailedMatchModel(**match_model.model_dump(), xGD=xGD)
