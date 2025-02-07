from app.core.external_services import NorskTippingAPI

class MatchesService:
	def __init__(self):
		self.norsk_tipping_api = NorskTippingAPI()

	async def get_coming_matches(self):
		return await self.norsk_tipping_api.get_coming_matches()
	
	async def close(self):
		await self.norsk_tipping_api.close()