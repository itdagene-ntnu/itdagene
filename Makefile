fixme:
	docker run --rm -v ${PWD}:/code -it python:3.9-slim "bash" "-c" "cd /code && pip install -r requirements/black.txt -r requirements/isort.txt && isort itdagene && black itdagene"

.PHONY: fixme
