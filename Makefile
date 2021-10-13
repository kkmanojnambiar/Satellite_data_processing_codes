docker_build:
	docker build . -t kkmanojnambiar/wrf_postprocessing_codes

docker_run:
	docker run -d --name wrf_postprocessing_codes --mount type=bind,source="$$(pwd)/",target=/wrf_postprocessing_codes kkmanojnambiar/wrf_postprocessing_codes

docker_shell:
	docker exec -it wrf_postprocessing_codes /bin/bash

docker_stop:
	docker stop wrf_postprocessing_codes

docker_remove:
	docker rm wrf_postprocessing_codes

docker_push:
	docker push kkmanojnambiar/wrf_postprocessing_codes:latest

docker_logs:
	docker logs wrf_postprocessing_codes

docker_prune:
	docker system prune -a

formatting:
	safety check
	isort .
	black .
	flake8 .

generate_documentation:
	pdoc --html --output-dir docs --force . 

open_documentation:
	open docs/wrf_postprocessing_codes/index.html

