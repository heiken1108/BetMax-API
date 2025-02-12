from dataclasses import dataclass
from typing import Dict
import pandas as pd
from app.core.schemas import ELOProbs

@dataclass
class TeamRatingsRepository:
    """Handles access to team ELO ratings data"""
    elo_ratings: pd.DataFrame
    name_mapping: Dict[str, str]
    default_elo: float = 1499

    @classmethod
    def from_csv(cls, filepath: str, name_mapping: Dict[str, str]) -> 'TeamRatingsRepository':
        return cls(
            elo_ratings=pd.read_csv(filepath, index_col=0),
            name_mapping=name_mapping
        )

    def get_elo_rating(self, team_name: str) -> float:
        if not team_name:
            return self.default_elo
        mapped_name = self.name_mapping.get(team_name, team_name)
        try:
            return self.elo_ratings.loc[mapped_name]['Elo']
        except KeyError:
            return self.default_elo

class FixturesRepository:
    """Handles access to fixtures and probability data"""
    def __init__(self, fixtures_df: pd.DataFrame):
        self.fixtures = fixtures_df

    @classmethod
    def from_csv(cls, filepath: str) -> 'FixturesRepository':
        return cls(pd.read_csv(filepath, index_col=['Home', 'Away']))

    def get_match_probabilities(self, home_team: str, away_team: str, name_mapping: Dict[str, str]) -> ELOProbs:
        if not home_team or not away_team:
            return ELOProbs(home_prob=0, draw_prob=0, away_prob=0)
            
        home = name_mapping.get(home_team, home_team)
        away = name_mapping.get(away_team, away_team)
        
        try:
            row = self.fixtures.loc[home, away]
            return ELOProbs(
                home_prob=sum(row[f'GD={i}'] for i in range(1, 6)) + row['GD>5'],
                draw_prob=row['GD=0'],
                away_prob=sum(row[f'GD={-i}'] for i in range(1, 6)) + row['GD<-5']
            )
        except KeyError:
            return ELOProbs(home_prob=0, draw_prob=0, away_prob=0)