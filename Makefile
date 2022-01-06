python = python3.10

.PHONY: lint
lint:
	$(python) -m no_init musictool_stream tests
	$(python) -m force_absolute_imports musictool_stream tests
	$(python) -m isort --force-single-line-imports musictool_stream tests
	$(python) -m autoflake --recursive --in-place musictool_stream tests
	$(python) -m autopep8 --in-place --recursive --aggressive --ignore=E221,E401,E402,E501,W503,E701,E704,E721,E741,I100,I201,W504 --exclude=musictool_stream/util/wavfile.py musictool_stream tests
	$(python) -m unify --recursive --in-place musictool_stream tests
	$(python) -m flake8 --ignore=E221,E501,W503,E701,E704,E741,I100,I201,W504 --exclude=musictool_stream/util/wavfile.py musictool_stream tests

.PHONY: messages
messages:
	git log --pretty='%ad %h %s' --date=unix > static/messages.txt

.PHONY: test
test:
	$(python) -m pytest -vv --cov=musictool tests

.PHONY: build_push_stream
build_push_stream: messages
	make messages
	#docker buildx build --platform linux/arm64/v8,linux/amd64 --tag tandav/musictool-stream -f --push .
	docker build --tag tandav/musictool-stream .
	docker push tandav/musictool-stream
