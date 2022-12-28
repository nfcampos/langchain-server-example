.PHONY: = start

start:
	poetry run uvicorn langchain_server_example:app --reload --port 8001