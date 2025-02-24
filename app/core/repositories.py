from dataclasses import dataclass
from typing import Dict
import pandas as pd
from .schemas import HUBModel, BoolModel

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
    def __init__(self, fixtures_df: pd.DataFrame, name_mapping: Dict[str, str]):
        self.fixtures = fixtures_df
        self.name_mapping = name_mapping

    @classmethod
    def from_csv(cls, filepath: str, name_mapping: Dict[str, str]) -> 'FixturesRepository':
        return cls(pd.read_csv(filepath, index_col=['Home', 'Away']), name_mapping=name_mapping)


    def _get_hub_probs(self, home_team: str, away_team: str, home_cols: list, draw_cols: list, away_cols: list) -> HUBModel:
        try:
            home = self.name_mapping.get(home_team, home_team)
            away = self.name_mapping.get(away_team, away_team)
            row = self.fixtures.loc[home, away]
            return HUBModel(
                home=sum(row[col] for col in home_cols),
                draw=sum(row[col] for col in draw_cols),
                away=sum(row[col] for col in away_cols)
            )
        except KeyError:
            return HUBModel(home=0, draw=0, away=0)
    
    def _get_bool_probs(self, home_team: str, away_team: str, true_cols: list, false_cols: list) -> BoolModel:
        try:
            home = self.name_mapping.get(home_team, home_team)
            away = self.name_mapping.get(away_team, away_team)
            row = self.fixtures.loc[home, away]
            return BoolModel(
                true=sum(row[col] for col in true_cols),
                false=sum(row[col] for col in false_cols)
            )
        except KeyError:
            return BoolModel(true=0, false=0)


    def get_match_probabilities(self, home_team: str, away_team: str) -> HUBModel:
        home_cols = ['GD=1', 'GD=2', 'GD=3', 'GD=4', 'GD=5', 'GD>5']
        draw_cols = ['GD=0']
        away_cols = ['GD=-1', 'GD=-2', 'GD=-3', 'GD=-4', 'GD=-5', 'GD<-5']

        return self._get_hub_probs(home_team, away_team, home_cols, draw_cols, away_cols)
    
    def get_total_goals_over_05_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:0-1','R:1-0','R:0-2','R:1-1','R:2-0','R:0-3','R:1-2','R:2-1','R:3-0','R:0-4','R:1-3','R:2-2','R:3-1','R:4-0','R:0-5','R:1-4','R:2-3','R:3-2','R:4-1','R:5-0','R:0-6','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1','R:6-0']
        false_cols = ['R:0-0']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)

    def get_total_goals_over_15_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:0-2','R:1-1','R:2-0','R:0-3','R:1-2','R:2-1','R:3-0','R:0-4','R:1-3','R:2-2','R:3-1','R:4-0','R:0-5','R:1-4','R:2-3','R:3-2','R:4-1','R:5-0','R:0-6','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1','R:6-0']
        false_cols = ['R:0-0','R:0-1','R:1-0']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)

    def get_total_goals_over_25_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:0-3','R:1-2','R:2-1','R:3-0','R:0-4','R:1-3','R:2-2','R:3-1','R:4-0','R:0-5','R:1-4','R:2-3','R:3-2','R:4-1','R:5-0','R:0-6','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1','R:6-0']
        false_cols = ['R:0-0','R:0-1','R:1-0','R:0-2','R:1-1','R:2-0']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)

    def get_total_goals_over_35_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:0-4','R:1-3','R:2-2','R:3-1','R:4-0','R:0-5','R:1-4','R:2-3','R:3-2','R:4-1','R:5-0','R:0-6','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1','R:6-0']
        false_cols = ['R:0-0','R:0-1','R:1-0','R:0-2','R:1-1','R:2-0','R:0-3','R:1-2','R:2-1','R:3-0']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)

    def get_total_goals_over_45_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:0-5','R:1-4','R:2-3','R:3-2','R:4-1','R:5-0','R:0-6','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1','R:6-0']
        false_cols = ['R:0-0','R:0-1','R:1-0','R:0-2','R:1-1','R:2-0','R:0-3','R:1-2','R:2-1','R:3-0','R:0-4','R:1-3','R:2-2','R:3-1','R:4-0']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)

    def get_total_goals_over_55_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:0-6','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1','R:6-0']
        false_cols = ['R:0-0','R:0-1','R:1-0','R:0-2','R:1-1','R:2-0','R:0-3','R:1-2','R:2-1','R:3-0','R:0-4','R:1-3','R:2-2','R:3-1','R:4-0','R:0-5','R:1-4','R:2-3','R:3-2','R:4-1','R:5-0']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)
    
    def get_total_home_goals_over_05_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:1-0','R:1-1','R:2-0','R:1-2','R:2-1','R:3-0','R:1-3','R:2-2','R:3-1','R:4-0','R:1-4','R:2-3','R:3-2','R:4-1','R:5-0','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1','R:6-0']
        false_cols = ['R:0-0','R:0-1','R:0-2','R:0-3','R:0-4','R:0-5','R:0-6']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)
    
    def get_total_home_goals_over_15_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:2-0','R:2-1','R:3-0','R:2-2','R:3-1','R:4-0','R:2-3','R:3-2','R:4-1','R:5-0','R:2-4','R:3-3','R:4-2','R:5-1','R:6-0']
        false_cols = ['R:0-0','R:0-1','R:0-2','R:0-3','R:0-4','R:0-5','R:0-6','R:1-0','R:1-1','R:1-2','R:1-3','R:1-4','R:1-5']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)
    
    def get_total_home_goals_over_25_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:3-0','R:3-1','R:4-0','R:3-2','R:4-1','R:5-0','R:3-3','R:4-2','R:5-1','R:6-0']
        false_cols = ['R:0-0','R:0-1','R:0-2','R:0-3','R:0-4','R:0-5','R:0-6','R:1-0','R:1-1','R:1-2','R:1-3','R:1-4','R:1-5','R:2-0','R:2-1','R:2-2','R:2-3','R:2-4']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)
    
    def get_total_away_goals_over_05_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:0-1','R:0-2','R:0-3','R:0-4','R:0-5','R:0-6','R:1-1','R:1-2','R:2-1','R:1-3','R:2-2','R:3-1','R:1-4','R:2-3','R:3-2','R:4-1','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1']
        false_cols = ['R:0-0','R:1-0','R:2-0','R:3-0','R:4-0','R:5-0','R:6-0']

        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)

    def get_total_away_goals_over_15_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:0-2','R:0-3','R:0-4','R:0-5','R:0-6','R:1-2','R:1-3','R:2-2','R:1-4','R:2-3','R:3-2','R:1-5','R:2-4','R:3-3','R:4-2']
        false_cols = ['R:0-0','R:1-0','R:2-0','R:3-0','R:4-0','R:5-0','R:6-0','R:0-1','R:1-1','R:2-1','R:3-1','R:4-1','R:5-1']

        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)
    
    def get_total_away_goals_over_25_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:0-3','R:0-4','R:0-5','R:0-6','R:1-3','R:1-4','R:2-3','R:1-5','R:2-4','R:3-3']
        false_cols = ['R:0-0','R:1-0','R:2-0','R:3-0','R:4-0','R:5-0','R:6-0','R:0-1','R:1-1','R:2-1','R:3-1','R:4-1','R:5-1','R:0-2','R:1-2','R:2-2','R:3-2','R:4-2']

        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)
    
    
    def get_total_goals_odd_even_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:0-1', 'R:1-0', 'R:0-3', 'R:1-2', 'R:2-1', 'R:3-0', 'R:5-0', 'R:4-1', 'R:3-2', 'R:2-3', 'R:1-4', 'R:0-5']
        false_cols = ['R:0-0','R:2-0', 'R:1-1', 'R:0-2', 'R:4-0', 'R:3-1', 'R:2-2', 'R:1-3', 'R:0-4', 'R:6-0', 'R:5-1', 'R:4-2', 'R:3-3', 'R:2-4', 'R:1-5', 'R:0-6']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)
    
    def get_both_teams_to_score_probs(self, home_team: str, away_team: str) -> BoolModel:        
        true_cols = ['R:1-1', 'R:2-1', 'R:1-2', 'R:3-1', 'R:2-2', 'R:1-3', 'R:4-1', 'R:3-2', 'R:2-3', 'R:1-4', 'R:5-1', 'R:4-2', 'R:3-3', 'R:2-4', 'R:1-5']
        false_cols = ['R:0-0', 'R:1-0', 'R:2-0', 'R:3-0', 'R:4-0', 'R:5-0', 'R:6-0','R:0-1', 'R:0-2', 'R:0-3', 'R:0-4', 'R:0-5', 'R:0-6']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)
    
    def get_home_clean_sheet_probs(self, home_team: str, away_team: str) -> BoolModel:     
        true_cols = ['R:0-0','R:1-0','R:2-0','R:3-0','R:4-0','R:5-0','R:6-0']   
        false_cols = ['R:0-1','R:0-2','R:1-1','R:0-3','R:1-2','R:2-1','R:0-4','R:1-3','R:2-2','R:3-1','R:0-5','R:1-4','R:2-3','R:3-2','R:4-1','R:0-6','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)
    
    def get_away_clean_sheet_probs(self, home_team: str, away_team: str) -> BoolModel: 
        true_cols = ['R:0-0','R:0-1','R:0-2','R:0-3','R:0-4','R:0-5','R:0-6']    
        false_cols = ['R:1-0','R:1-1','R:2-0','R:1-2','R:2-1','R:3-0','R:1-3','R:2-2','R:3-1','R:4-0','R:1-4','R:2-3','R:3-2','R:4-1','R:5-0','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1','R:6-0']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)
    
    def get_home_win_and_clean_sheet_probs(self, home_team: str, away_team: str) -> BoolModel:     
        true_cols = ['R:1-0','R:2-0','R:3-0','R:4-0','R:5-0','R:6-0']   
        false_cols = ['R:0-0','R:0-1','R:0-2','R:1-1','R:0-3','R:1-2','R:2-1','R:0-4','R:1-3','R:2-2','R:3-1','R:0-5','R:1-4','R:2-3','R:3-2','R:4-1','R:0-6','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)
    
    def get_away_win_and_clean_sheet_probs(self, home_team: str, away_team: str) -> BoolModel: 
        true_cols = ['R:0-1','R:0-2','R:0-3','R:0-4','R:0-5','R:0-6']    
        false_cols = ['R:0-0','R:1-0','R:1-1','R:2-0','R:1-2','R:2-1','R:3-0','R:1-3','R:2-2','R:3-1','R:4-0','R:1-4','R:2-3','R:3-2','R:4-1','R:5-0','R:1-5','R:2-4','R:3-3','R:4-2','R:5-1','R:6-0']
        
        return self._get_bool_probs(home_team, away_team, true_cols, false_cols)

    
    def get_handicap_03_probs(self, home_team: str, away_team: str) -> HUBModel:
        home_cols = ['GD=4', 'GD=5', 'GD>5']
        draw_cols = ['GD=3']
        away_cols = ['GD<-5', 'GD=-5', 'GD=-4', 'GD=-3', 'GD=-2', 'GD=-1', 'GD=0', 'GD=1', 'GD=2']
        
        return self._get_hub_probs(home_team, away_team, home_cols, draw_cols, away_cols)
    
    def get_handicap_02_probs(self, home_team: str, away_team: str) -> HUBModel:
        home_cols = ['GD=3', 'GD=4', 'GD=5', 'GD>5']
        draw_cols = ['GD=2']
        away_cols = ['GD<-5', 'GD=-5', 'GD=-4', 'GD=-3', 'GD=-2', 'GD=-1', 'GD=0', 'GD=1']
        
        return self._get_hub_probs(home_team, away_team, home_cols, draw_cols, away_cols)
    
    def get_handicap_01_probs(self, home_team: str, away_team: str) -> HUBModel:
        home_cols = ['GD=2', 'GD=3', 'GD=4', 'GD=5', 'GD>5']
        draw_cols = ['GD=1']
        away_cols = ['GD<-5', 'GD=-5', 'GD=-4', 'GD=-3', 'GD=-2', 'GD=-1', 'GD=0']
        
        return self._get_hub_probs(home_team, away_team, home_cols, draw_cols, away_cols)
    
    def get_handicap_10_probs(self, home_team: str, away_team: str) -> HUBModel:
        home_cols = ['GD=0','GD=1','GD=2', 'GD=3', 'GD=4', 'GD=5', 'GD>5']
        draw_cols = ['GD=-1']
        away_cols = ['GD<-5', 'GD=-5', 'GD=-4', 'GD=-3', 'GD=-2']
        
        return self._get_hub_probs(home_team, away_team, home_cols, draw_cols, away_cols)

    def get_handicap_20_probs(self, home_team: str, away_team: str) -> HUBModel:
        home_cols = ['GD=-1', 'GD=0','GD=1','GD=2', 'GD=3', 'GD=4', 'GD=5', 'GD>5']
        draw_cols = ['GD=-2']
        away_cols = ['GD<-5', 'GD=-5', 'GD=-4', 'GD=-3']
        
        return self._get_hub_probs(home_team, away_team, home_cols, draw_cols, away_cols)
