fixme:
	docker run --rm -v ${PWD}:/code -it python:3.7-slim "bash" "-c" "cd /code && pip install -r requirements/black.txt -r requirements/isort.txt && isort -rc itdagene && black itdagene"

.PHONY: fixme
