PHONY: install-requirements
install-requirements:
	pip install -r requirements.txt

PHONY: run-api-locally
run-api-locally: install-requirements
	OFFLINE=true uvicorn app.main:fastapi_app --reload --host 0.0.0.0

PHONY: generate-openapi
generate-openapi:
	python generate-openapi.py > openapi.json

PHONY: format
format:
	black app && \
	isort app

PHONY: test
test:
	OFFLINE=true python -m pytest app/tests/