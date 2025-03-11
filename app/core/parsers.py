from datetime import datetime
from typing import Dict, Optional
from .schemas import MatchSummaryModel, ELOModel, MatchDetailModel, HUBModel, MarketModel, BoolModel
from .repositories import TeamRatingsRepository, FixturesRepository
from app.utils.utils import tournaments_of_interest

class MatchParser:
    """Handles parsing of raw match data into MatchModel objects"""
    def __init__(self, ratings_repo: TeamRatingsRepository, fixtures_repo: FixturesRepository):
        self.ratings_repo = ratings_repo
        self.fixtures_repo = fixtures_repo
        self.market_parsers = {
            'HUB': self.fixtures_repo.get_match_probabilities,
            'Totalt antall mål - Over/Under 0.5': self.fixtures_repo.get_total_goals_over_05_probs,
            'Totalt antall mål - Over/Under 1.5': self.fixtures_repo.get_total_goals_over_15_probs,
            'Totalt antall mål - Over/Under 2.5': self.fixtures_repo.get_total_goals_over_25_probs,
            'Totalt antall mål - Over/Under 3.5': self.fixtures_repo.get_total_goals_over_35_probs,
            'Totalt antall mål - Over/Under 4.5': self.fixtures_repo.get_total_goals_over_45_probs,
            'Totalt antall mål - Over/Under 5.5': self.fixtures_repo.get_total_goals_over_55_probs,
            'Totalt antall mål - oddetall/partall': self.fixtures_repo.get_total_goals_odd_even_probs,
            'Totalt antall home mål over/under 0.5': self.fixtures_repo.get_total_home_goals_over_05_probs,
            'Totalt antall home mål over/under 1.5': self.fixtures_repo.get_total_home_goals_over_15_probs,
            'Totalt antall home mål over/under 2.5': self.fixtures_repo.get_total_home_goals_over_25_probs,
            'Totalt antall away mål over/under 0.5': self.fixtures_repo.get_total_away_goals_over_05_probs,
            'Totalt antall away mål over/under 1.5': self.fixtures_repo.get_total_away_goals_over_15_probs,
            'Totalt antall away mål over/under 2.5': self.fixtures_repo.get_total_away_goals_over_25_probs,
            'home holder nullen': self.fixtures_repo.get_home_clean_sheet_probs,
            'away holder nullen': self.fixtures_repo.get_away_clean_sheet_probs,
            'home vinner og holder nullen': self.fixtures_repo.get_home_win_and_clean_sheet_probs,
            'away vinner og holder nullen': self.fixtures_repo.get_away_win_and_clean_sheet_probs,
            'Begge lag scorer': self.fixtures_repo.get_both_teams_to_score_probs,
            'Handikap 3-veis 0:3': self.fixtures_repo.get_handicap_03_probs,
            'Handikap 3-veis 0:2': self.fixtures_repo.get_handicap_02_probs,
            'Handikap 3-veis 0:1': self.fixtures_repo.get_handicap_01_probs,
            'Handikap 3-veis 1:0': self.fixtures_repo.get_handicap_10_probs,
            'Handikap 3-veis 2:0': self.fixtures_repo.get_handicap_20_probs,
        }

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

    def parse_odds(self, market_data: Dict) -> Optional[HUBModel]:
        if not market_data:
            return None
            
        selections = market_data.get('selections', [])
        if len(selections) < 3:
            return None
            
        try:
            return HUBModel(
                home=selections[0].get('selectionOdds', 0),
                draw=selections[1].get('selectionOdds', 0),
                away=selections[2].get('selectionOdds', 0)
            )
        except (IndexError, TypeError):
            return None

    def parse_match(self, match: Dict) -> Optional[MatchSummaryModel]:
        if not self.is_valid_match(match):
            return None

        try:
            NT_id = match.get("eventId", '')
            home_team = match.get("homeParticipant", '')
            away_team = match.get("awayParticipant", '')
            start_time = datetime.fromisoformat(match.get("startTime", ''))
            tournament = match.get("tournament", {}).get("name", '')
            odds = self.parse_odds(match.get('mainMarket', {}))
            probs = self.fixtures_repo.get_match_probabilities(
                home_team, 
                away_team, 
            )
            elo = ELOModel(
                home_elo=self.ratings_repo.get_elo_rating(home_team),
                away_elo=self.ratings_repo.get_elo_rating(away_team),
                probs=probs
            )
            expected_value = HUBModel(
                home=odds.home * probs.home,
                draw=odds.draw * probs.draw,
                away=odds.away * probs.away
            )
            
            if not odds or not probs or (probs.home == 0 and probs.draw == 0 and probs.away == 0):
                return None

            return MatchSummaryModel(
                NT_id=NT_id,
                home_team=home_team,
                away_team=away_team,
                start_time=start_time,
                tournament=tournament,
                odds=odds,
                elo=elo,
                expected_value=expected_value
            )
        except (ValueError, TypeError, KeyError) as e:
            print(f"Error parsing match: {e}")  # You might want to use proper logging here
            return None
    
    def parse_detailed_match(self, match: Dict, markets: list) -> Optional[MatchDetailModel]:
        try:
            NT_id = match.get("eventId", '')
            home_team = match.get("homeParticipant", '')
            away_team = match.get("awayParticipant", '')
            start_time=datetime.fromisoformat(match.get("startTime", ''))
            tournament=match.get("tournament", {}).get("name", '')
            probs = self.fixtures_repo.get_match_probabilities(
                home_team, 
                away_team, 
            )
            markets = [processed_market for market in markets if (processed_market := self.parse_market(market, home_team, away_team)) is not None]
            elo=ELOModel(
                home_elo=self.ratings_repo.get_elo_rating(home_team),
                away_elo=self.ratings_repo.get_elo_rating(away_team),
                probs=probs
            )
            return MatchDetailModel(
                NT_id=NT_id,
                home_team=home_team,
                away_team=away_team,
                start_time=start_time,
                tournament=tournament,
                markets=markets,
                elo=elo
            )
        except (ValueError, TypeError, KeyError) as e:
            print(f"Error parsing match: {e}")  # You might want to use proper logging here
            return None
        
    def parse_market(self, market: Dict, home_team: str, away_team: str) -> Optional[MarketModel]:
        market_name = market.get('marketName', '')
        selections = market.get('selections', [])
        if len(selections) < 2:
            return None
        elif len(selections) == 2:
            odds = BoolModel(true=selections[0].get('selectionOdds'), false=selections[1].get('selectionOdds'))
            market_name = market_name.replace(home_team, 'home').replace(away_team, 'away')
            market_parser = self.market_parsers.get(market_name, lambda *args, **kwargs: None)
            probs = market_parser(home_team, away_team)
            if probs is None:
                return None
            probs = BoolModel(true=probs.true, false=probs.false)
            expected_value = BoolModel(true=odds.true * probs.true, false=odds.false * probs.false)
            return MarketModel(name=market_name, selections=odds, probs=probs, expected_value=expected_value)
        elif len(selections) == 3:
            odds = HUBModel(home=selections[0].get('selectionOdds'), draw=selections[1].get('selectionOdds'), away=selections[2].get('selectionOdds'))
            market_parser = self.market_parsers.get(market_name, lambda *args, **kwargs: None)
            probs = market_parser(home_team, away_team)
            if probs is None:
                return None
            probs = HUBModel(home=probs.home, draw=probs.draw, away=probs.away)
            expected_value = HUBModel(home=odds.home * probs.home,draw=odds.draw * probs.draw,away=odds.away * probs.away)
            return MarketModel(name=market_name, selections=odds, probs=probs, expected_value=expected_value)
        else:
            return None

