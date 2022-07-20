LINTING_DIRS := musictool_stream tests

.PHONY: stream_docker
stream_docker:
	docker run --pull=always --rm -it -v $$PWD/credentials.py:/app/credentials.py tandav/musictool-stream

.PHONY: stream
stream:
	python -m musictool_stream.daw video

.PHONY: test_video
test_video:
	python -m musictool_stream.daw video_test

.PHONY: fix-lint
fix-lint:
	python -m autoflake --recursive --in-place musictool_stream tests

.PHONY: check-lint
check-lint:
	#$(python) -m no_init --allow-empty $(LINTING_DIRS)
	$(python) -m force_absolute_imports $(LINTING_DIRS)
	$(python) -m isort --check-only $(LINTING_DIRS)
	$(python) -m autoflake --recursive $(LINTING_DIRS)
	$(python) -m autopep8 --diff $(LINTING_DIRS)
	$(python) -m flake8 $(LINTING_DIRS)
	#$(python) -m darglint --docstring-style numpy --verbosity 2 $(LINTING_DIRS)


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
