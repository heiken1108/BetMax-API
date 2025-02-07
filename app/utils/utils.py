import requests

def fetch_data_from_api(url) -> dict:
	response = requests.get(url)
	if response.status_code == 200:
		return response.json()
	else:
		return {"error": "Failed to load data from external source."}