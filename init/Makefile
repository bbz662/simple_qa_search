env:
	cp .env.example .env
build:
	docker compose build
init_db:
	docker compose run myapp python make_table.py
insert_data:
	docker compose run myapp python make_data.py
move_data:
	cp ./data/qa_pairs.db ../qa_pairs.db