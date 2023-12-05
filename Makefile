
install:
	pipenv install

dev:
	uvicorn magicpost.app:app --reload

demo:
	python -m magicpost.app