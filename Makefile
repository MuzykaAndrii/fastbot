up:
	docker compose --env-file ./secrets/environment/.dev.env up --build -d
down:
	docker compose down
test:
	docker exec -t fastbot-app pytest -v -s -W ignore::DeprecationWarning
tunnel:
	ngrok http 8000
logs:
	docker logs --follow fastbot-app