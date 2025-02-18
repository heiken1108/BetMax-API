from app.core.schemas import ELOProbs
tournaments_of_interest = ['England - Premier League', 'Italia - Serie A', 'Frankrike -  Ligue 1', 'Spania - Primera Division', 'Tyskland - Bundesliga', 'Internasjonal klubb - UEFA Champions League']
DRAW_FACTOR = 0.36 #0.36 i LaLiga
HOME_ADVANTAGE = 65 #65 i LaLiga

NT_to_ClubELO_names_mapping = {
	'Blackburn Rovers': 'Blackburn',
	'Plymouth Argyle': 'Plymouth',
	'Aston Villa': 'Aston Villa',
	'Tottenham Hotspur': 'Tottenham',
	'Wolverhampton Wanderers': 'Wolves',
	'Liverpool FC': 'Liverpool',
	'Liverpool': 'Liverpool',
	'Everton': 'Everton',
	'Brighton and Hove Albion': 'Brighton',
	'Leicester City': 'Leicester',
	'Atalanta BC': 'Atalanta',
	'FC St. Pauli': 'St Pauli',
	'VfB Stuttgart': 'Stuttgart',
	'VfL Wolfsburg': 'Wolfsburg',
	'Borussia Mönchengladbach': 'Gladbach',
	'VfL Bochum': 'Bochum',
	'Borussia Dortmund': 'Dortmund',
	'Ipswich Town': 'Ipswich',
	'Manchester City': 'Man City',
	'Newcastle United': 'Newcastle',
	'West Ham United': 'West Ham',
	'Nottingham Forest': "Forest",
	'Bayer Leverkusen': 'Leverkusen',
	'Bayern München': 'Bayern',
	'Atletico Madrid': 'Atletico',
	'Celta Vigo': 'Celta',
	'Hellas Verona FC': 'Verona',
	'Athletic Club Bilbao': 'Bilbao',
	'AC Monza': 'Monza',
	'Werder Bremen': 'Werder',
	'TSG Hoffenheim': 'Hoffenheim',
	'Real Valladolid': 'Valladolid',
	'Eintracht Frankfurt': 'Frankfurt',
	'Holstein Kiel': 'Holstein',
	'Manchester United': 'Man United',
	'Parma FC': 'Parma',
	'1. FC Heidenheim': 'Heidenheim',
	'FSV Mainz': 'Mainz',
	'Real Betis': 'Betis',
	'Real Sociedad': 'Sociedad',
	'Club Brugge': 'Brugge',
	'AS Monaco': 'Monaco',
	'Sporting CP': 'Sporting',
	'FC Porto': 'Porto',
	'Paris Saint Germain': 'Paris SG',
	'PSV Eindhoven': 'PSV',
}

#Not in use
def calculate_elo_probs(home_elo: float, away_elo: float):
	elo_diff = home_elo + HOME_ADVANTAGE - away_elo
	prob_home_without_draws = 1 / (1 + 10 ** (-elo_diff / 400))
	prob_away_without_draws = 1 / (1 + 10 ** (elo_diff / 400))
	prob_draw = DRAW_FACTOR * (
		1 - abs(prob_home_without_draws - prob_away_without_draws)
	)
	prob_home = prob_home_without_draws - prob_draw / 2
	prob_away = prob_away_without_draws - prob_draw / 2
	return ELOProbs(home_prob=prob_home, draw_prob=prob_draw, away_prob=prob_away)



