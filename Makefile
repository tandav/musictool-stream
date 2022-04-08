.PHONY: stream_docker
stream_docker:
	docker run --pull=always --rm -it -v $$PWD/credentials.py:/app/credentials.py tandav/musictool-stream

.PHONY: stream
stream:
	python -m musictool_stream.daw video

.PHONY: test_video
test_video:
	python -m musictool_stream.daw video_test

.PHONY: lint
lint:
	python -m no_init musictool_stream tests
	python -m force_absolute_imports musictool_stream tests
	python -m isort --force-single-line-imports musictool_stream tests
	python -m autoflake --recursive --in-place musictool_stream tests
	python -m autopep8 --in-place --recursive --aggressive --ignore=E221,E401,E402,E501,W503,E701,E704,E721,E741,I100,I201,W504 --exclude=musictool_stream/util/wavfile.py musictool_stream tests
	python -m unify --recursive --in-place musictool_stream tests
	python -m flake8 --ignore=E221,E501,W503,E701,E704,E741,I100,I201,W504 --exclude=musictool_stream/util/wavfile.py musictool_stream tests

.PHONY: messages
messages:
	git log --pretty='%ad %h %s' --date=unix > static/messages.txt

.PHONY: test
test:
	python -m pytest tests

.PHONY: build_push_base
build_push_base:
	# docker buildx build --no-cache
	docker buildx build --platform linux/arm64/v8,linux/amd64 --tag tandav/musictool-stream-base --file docker/base --push .
#	docker build --tag tandav/musictool-stream-base --file docker/base .
	#docker push tandav/musictool-stream-base

.PHONY: build_push
build_push: messages
	make messages
	#docker buildx build --platform linux/arm64/v8,linux/amd64 --tag tandav/musictool-stream -f --push .
	docker build --tag tandav/musictool-stream .
	docker push tandav/musictool-stream

.PHONY: upload_creds_makefile
upload_creds_makefile:
	scp credentials.py Makefile cn:~/musictool

.PHONY: daw
daw:
	python -m musictool_stream.daw

.PHONY:  file
file: ## render 4 seconds to a file for test
	python -m musictool_stream.daw video_file 4

.PHONY: help
help: ## Display this help
	@grep -E '^[ a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'


.PHONY: generate
generate:
	docker run --rm -it -v $$PWD:/app -v /home/ubuntu/musictool-labeling/static:/app/static --workdir /app tandav/musictool-stream-base python generate.py
