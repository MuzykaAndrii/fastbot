up:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
tunnel:
	ngrok http 8000