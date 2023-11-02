.PHONY: start
start:
	uvicorn app.main:app --reload --port 9001 --host 0.0.0.0

install:
	pip install -r requirements.txt

.PHONY: test
test:
	pytest tests