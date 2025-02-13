from typing import Optional
from asyncio import Task
import aiohttp
import pandas as pd
import io
import os
import asyncio
from datetime import date

class DataUpdater:
	def __init__(self):
		self.elo_rating_url = f"http://api.clubelo.com/{date.today().isoformat()}"
		self.fixtures_url = "http://api.clubelo.com/Fixtures"
		self.elo_csv_path = "app/files/elo_ratings.csv"
		self.fixtures_csv_path = "app/files/fixtures.csv"
		self.update_task: Optional[Task] = None
		self._stop_flag = False
	
	async def download_elo_csv(self) -> bool:
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(self.elo_rating_url) as response:
					if response.status == 200:
						data = await response.text()
						df = pd.read_csv(io.StringIO(data)) 
						df.set_index('Club', inplace=True)
						os.makedirs(os.path.dirname(self.elo_csv_path), exist_ok=True)
						df.to_csv(self.elo_csv_path)
						print(f"CSV downloaded and saved to {self.elo_csv_path}")
						return True
					else:
						print(f"Failed to fetch CSV: {response.status}")
						return False
		except Exception as e:
			print(f"Error downloading ELO CSV: {e}")
			return False
		
	async def download_fixtures_csv(self) -> bool:
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(self.fixtures_url) as response:
					if response.status == 200:
						data = await response.text()
						df = pd.read_csv(io.StringIO(data), index_col=['Home', 'Away'])
						os.makedirs(os.path.dirname(self.fixtures_csv_path), exist_ok=True)
						df.to_csv(self.fixtures_csv_path)
						print(f"CSV downloaded and saved to {self.fixtures_csv_path}")
						return True
					else:
						print(f"Failed to fetch CSV: {response.status}")
						return False
		except Exception as e:
			print(f"Error downloading fixtures CSV: {e}")
			return False
		
	async def update_loop(self):
		while not self._stop_flag:
			try:
				await asyncio.gather(
					self.download_elo_csv(),
					self.download_fixtures_csv()
				)
				await asyncio.sleep(60*60*24) #Vil egentlig ha ved et fikset tidspunkt hver dag
			except Exception as e:
				print(f"Error in update loop: {e}")
				await asyncio.sleep(5)
	
	async def start(self):
		self._stop_flag = False
		self.update_task = asyncio.create_task(self.update_loop())
	
	async def stop(self):
		if self.update_task:
			self._stop_flag = True
			self.update_task.cancel()
			try:
				await self.update_task
			except asyncio.CancelledError:
				pass
			self.update_task = None