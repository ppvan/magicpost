
install:
	pipenv install

dev:
	uvicorn magicpost.app:app --reload

test:
	pytest

demo:
	python -m magicpost.app