from abc import ABC, abstractmethod
import aiohttp

class ExternalDataSource(ABC):
	def __init__(self):
		self.session = aiohttp.ClientSession()

	@abstractmethod
	async def fetch_data(self, extension: str) -> dict:
		pass

	async def close(self):
		await self.session.close()

class NorskTippingAPI(ExternalDataSource):
	async def fetch_data(self, extension) -> dict:
		async with self.session.get(
			f"https://api.norsk-tipping.no/OddsenGameInfo/v1/api/{extension}",
			headers={}
		) as response:
			response.raise_for_status()
			return await response.json()
		
	async def get_coming_matches(self):
		return await self.fetch_data("events/FBL")
	
class ClubELOAPI(ExternalDataSource):
	async def fetch_data(self, extension):
		async with self.session.get(
			f"https://api.clubelo.com/{extension}",
			headers={}
		) as response:
			response.raise_for_status()
			return await response.json()
		
	async def get_one_days_ranking(self, date): #Date på format YYYY-MM-DD
		return await self.fetch_data(date)
	
	async def get_one_clubs_rating_history(self, clubname):
		return await self.fetch_data(clubname)

	async def get_coming_fixtures(self):
		return await self.fetch_data("Fixtures")