remove:
	docker rmi niffler_backend_api:latest

build_local:
	docker build -f Dockerfile -t niffler_backend_api:latest .

run_img:
	docker run --env-file .env --rm --name niffler_backend_api_container -v ./api:/app/api -it niffler_backend_api:latest /bin/bash


run_api:
	docker run --env-file .env --rm --name niffler_backend_api_container \
	-v ./api:/app/api -v ./src:/app/src -p 8087:8087 -it niffler_backend_api:latest \
	uvicorn api.main:app --host 0.0.0.0 --port 8087 --reload

run_push_docker_hub:
	docker tag niffler_backend_api:latest ymcsabo/niffler_backend_api:latest && \
	docker push ymcsabo/niffler_backend_api:latest