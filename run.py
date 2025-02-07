import uvicorn
from dotenv import load_dotenv
import os

env_file = ".env.production" if os.getenv("ENV") == "production" else ".env"
load_dotenv(env_file)

if __name__ == "__main__":
	uvicorn.run(
		"app.main:app",
		host=os.getenv("HOST"),
		port=int(os.getenv("PORT", 8000)),
		reload=os.getenv("DEBUG", "False").lower() == "true"
	)