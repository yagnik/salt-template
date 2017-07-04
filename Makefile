docker-compose:
	which docker-compose

docker-start: docker-compose
	docker-compose build --force-rm
	docker-compose up -d

docker-stop: docker-compose
	docker-compose down
	docker-compose rm

setup: docker-start

clean: docker-stop

test-style: docker-start
	docker exec -it salttemplate_masterless_1 flake8 .

test-master: docker-start
	docker exec -it salttemplate_master_1 pytest -v -p no:cacheprovider

test-masterless: docker-start
	docker exec -it salttemplate_masterless_1 pytest -v -p no:cacheprovider

test: docker-start test-masterless test-master test-style

script:
	./scripts/generate
