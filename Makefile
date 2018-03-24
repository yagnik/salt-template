docker-compose:
	@docker-compose version

docker-start: docker-compose
	docker-compose up -d

docker-stop: docker-compose
	docker-compose down
	docker-compose rm

setup: docker-start ## setup salt with docker containers for testing

clean: docker-stop ## clean all docker containers

test-style: docker-start ## test all style check
	docker exec salttemplate_masterless_1 flake8 .

test-master: docker-start ## test salt using master + minion
	docker exec salttemplate_master_1 pytest -v -p no:cacheprovider

test-masterless: docker-start ## test salt using masterless
	docker exec salttemplate_masterless_1 pytest -v -p no:cacheprovider

test: docker-start test-masterless test-master test-style

masterless-shell:  ## enter salt master container
	docker exec -it salttemplate_masterless_1 /bin/bash

master-shell:  ## enter salt master container
	docker exec -it salttemplate_master_1 /bin/bash

minion-shell:  ## enter salt master container
	docker exec -it salttemplate_minion_1 /bin/bash

help: ## display this help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
