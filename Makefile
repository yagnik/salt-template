docker-compose:
	which docker-compose

docker-start: docker-compose
	docker-compose build --force-rm
	docker-compose up -d

docker-stop: docker-compose
	docker-compose down
	docker-compose rm

setup: docker-start ## setup salt with docker containers for testing

clean: docker-stop ## clean all docker containers

test-style: docker-start ## test all style check
	docker exec -it salttemplate_masterless_1 flake8 .

test-master: docker-start ## test salt using master + minion
	docker exec -it salttemplate_master_1 pytest -v -p no:cacheprovider

test-masterless: docker-start ## test salt using masterless
	docker exec -it salttemplate_masterless_1 pytest -v -p no:cacheprovider

test: docker-start test-masterless test-master test-style

script:
	./scripts/generate

help: ## display this help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
