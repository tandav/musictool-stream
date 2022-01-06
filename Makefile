python = python3.10

.PHONY: messages
messages:
	git log --pretty='%ad %h %s' --date=unix > static/messages.txt

.PHONY: test
test:
	$(python) -m pytest -vv --cov=musictool tests

.PHONY: build_push_stream
build_push_stream: messages
	make messages
	#docker buildx build --platform linux/arm64/v8,linux/amd64 --tag tandav/musictool-stream -f ./Dockerfile-stream --push .
	docker build --tag tandav/musictool-stream -f ./Dockerfile-stream .
	docker push tandav/musictool-stream
